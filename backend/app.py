from flask import Flask, request, jsonify
import joblib
import pandas as pd
from model_utils import create_client_archetypes, generate_financial_story

app = Flask(__name__)

# Загружаем модели
stacking_model = joblib.load('final_stacking_model.pkl')
preprocessor = joblib.load('final_preprocessor.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    X = preprocessor.transform(df)
    pred_income = stacking_model.predict(X)[0]

    df = create_client_archetypes(df)
    archetype = df['dominant_archetype'][0]
    story = generate_financial_story(pred_income, archetype, df.get('age',0)[0])

    return jsonify({'predicted_income': float(pred_income), 'archetype': archetype, 'story': story})

if __name__ == '__main__':
    app.run(debug=True)


