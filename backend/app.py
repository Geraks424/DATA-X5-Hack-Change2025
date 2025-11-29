from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Загрузка моделей и препроцессора
preprocessor = joblib.load('final_preprocessor.pkl')
stacking_model = joblib.load('final_stacking_model.pkl')

numerical_features = ['age', 'turn_cur_cr_avg_v2', 'mob_cnt_days']
categorical_features = ['device_iphone_avg', 'vert_has_app_ru_tinkoff_investing']
all_features = numerical_features + categorical_features

@app.route('/')
def home():
    return "API работает! Используй POST /predict для прогноза дохода."

@app.route('/predict', methods=['POST'])
def predict_income():
    data = request.json
    missing_features = [f for f in all_features if f not in data]
    if missing_features:
        return jsonify({'error': f'Missing features: {missing_features}'}), 400

    input_df = pd.DataFrame([data])
    X_transformed = preprocessor.transform(input_df[all_features])
    predicted_income = stacking_model.predict(X_transformed)[0]

    return jsonify({'predicted_income': float(predicted_income)})

if __name__ == '__main__':
    app.run(debug=True)

