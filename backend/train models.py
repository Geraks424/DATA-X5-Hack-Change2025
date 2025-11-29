import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import RidgeCV

# Рабочие пути относительно расположения скрипта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')  # предполагается, что data/ на уровень выше
TRAIN_CSV = os.path.join(DATA_DIR, 'hackathon_income_train.csv')
TEST_CSV = os.path.join(DATA_DIR, 'hackathon_income_test.csv')

def main():
    # 1️⃣ Чтение данных
    train_data = pd.read_csv(TRAIN_CSV)
    test_data = pd.read_csv(TEST_CSV)

    # 2️⃣ Предобработка
    numerical_features = ['age','turn_cur_cr_avg_v2','mob_cnt_days']
    categorical_features = ['device_iphone_avg','vert_has_app_ru_tinkoff_investing']

    numerical_pipeline = Pipeline([('scaler', StandardScaler())])
    categorical_pipeline = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))])

    preprocessor = ColumnTransformer([
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

    # Fit preprocessor на тренировочном наборе перед сохранением
    preprocessor.fit(train_data[numerical_features + categorical_features])
    joblib.dump(preprocessor,'final_preprocessor.pkl')
    print("✅ final_preprocessor.pkl создан (fitted)")

    # 3️⃣ Базовые модели
    base_estimators = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('gbr', GradientBoostingRegressor(n_estimators=100, random_state=42))
    ]
    joblib.dump(base_estimators,'final_base_estimators.pkl')
    print("✅ final_base_estimators.pkl создан")

    # 4️⃣ Стекинг-модель (указываем final_estimator корректно)
    X_train = preprocessor.transform(train_data[numerical_features+categorical_features])
    y_train = train_data['income']

    stacking_model = StackingRegressor(
        estimators=base_estimators,
        final_estimator=RidgeCV(),  # надежный финальный регрессор
        passthrough=True
    )

    stacking_model.fit(X_train, y_train)
    joblib.dump(stacking_model,'final_stacking_model.pkl')
    print("✅ final_stacking_model.pkl создан")

    # 5️⃣ (опционально) Тестирование на тестовом наборе
    if 'income' in test_data.columns:
        X_test = preprocessor.transform(test_data[numerical_features+categorical_features])
        y_test = test_data['income']
        score = stacking_model.score(X_test, y_test)
        print(f"ℹ️ R² на тестовом наборе: {score:.4f}")

if __name__ == "__main__":
    main()