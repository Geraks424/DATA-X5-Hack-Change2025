from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Рабочий каталог относительно файла приложения
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREPROCESSOR_PATH = os.path.join(BASE_DIR, 'final_preprocessor.pkl')
STACKING_MODEL_PATH = os.path.join(BASE_DIR, 'final_stacking_model.pkl')

# Попытка загрузить модели безопасно
preprocessor = None
stacking_model = None
try:
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    logger.info(f"Loaded preprocessor from {PREPROCESSOR_PATH}")
except Exception as e:
    logger.error(f"Failed to load preprocessor: {e}")

try:
    stacking_model = joblib.load(STACKING_MODEL_PATH)
    logger.info(f"Loaded stacking model from {STACKING_MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load stacking model: {e}")

numerical_features = ['age', 'turn_cur_cr_avg_v2', 'mob_cnt_days']
categorical_features = ['device_iphone_avg', 'vert_has_app_ru_tinkoff_investing']
all_features = numerical_features + categorical_features

@app.route('/')
def home():
    return "API работает! Используй POST /predict для прогноза дохода."

@app.route('/predict', methods=['POST'])
def predict_income():
    if preprocessor is None or stacking_model is None:
        return jsonify({'error': 'Model or preprocessor not loaded on server.'}), 500

    try:
        data = request.get_json()
    except Exception:
        data = None

    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid JSON body'}), 400

    missing_features = [f for f in all_features if f not in data]
    if missing_features:
        return jsonify({'error': f'Missing features: {missing_features}'}), 400

    # Собираем DataFrame и приводим к числам (если возможно)
    input_df = pd.DataFrame([data], columns=all_features)
    for col in all_features:
        # Попробуем привести к числу, если не получится — оставим как есть (препроцессор должен уметь работать)
        try:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)
        except Exception:
            input_df[col] = input_df[col]

    try:
        X_transformed = preprocessor.transform(input_df[all_features])
    except Exception as e:
        logger.exception("Error transforming input with preprocessor")
        return jsonify({'error': f'Preprocessor transform error: {str(e)}'}), 500

    try:
        predicted_income = stacking_model.predict(X_transformed)[0]
    except Exception as e:
        logger.exception("Error predicting with stacking model")
        return jsonify({'error': f'Model prediction error: {str(e)}'}), 500

    return jsonify({'predicted_income': float(predicted_income)}), 200

if __name__ == '__main__':
    # Запуск на 0.0.0.0 полезен для Docker/внешнего доступа
    app.run(debug=True, host='0.0.0.0', port=5000)

