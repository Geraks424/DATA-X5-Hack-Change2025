import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor

def main():
    # 1️⃣ Чтение данных
    train_data = pd.read_csv('../data/hackathon_income_train.csv')
    test_data = pd.read_csv('../data/hackathon_income_test.csv')

    # 2️⃣ Предобработка
    numerical_features = ['age','turn_cur_cr_avg_v2','mob_cnt_days']
    categorical_features = ['device_iphone_avg','vert_has_app_ru_tinkoff_investing']

    numerical_pipeline = Pipeline([('scaler', StandardScaler())])
    categorical_pipeline = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer([
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ])

    joblib.dump(preprocessor,'final_preprocessor.pkl')
    print("✅ final_preprocessor.pkl создан")

    # 3️⃣ Базовые модели
    base_estimators = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
        ('gbr', GradientBoostingRegressor(n_estimators=100, random_state=42))
    ]
    joblib.dump(base_estimators,'final_base_estimators.pkl')
    print("✅ final_base_estimators.pkl создан")

    # 4️⃣ Оптимальные веса (пример вручную)
    optimal_weights = np.array([0.6,0.4])
    joblib.dump(optimal_weights,'final_optimal_weights.pkl')
    print("✅ final_optimal_weights.pkl создан")

    # 5️⃣ Стекинг-модель
    X_train = preprocessor.fit_transform(train_data[numerical_features+categorical_features])
    y_train = train_data['income']

    stacking_model = StackingRegressor(
        estimators=base_estimators,
        final_estimator=None,
        passthrough=True
    )

    stacking_model.fit(X_train, y_train)
    joblib.dump(stacking_model,'final_stacking_model.pkl')
    print("✅ final_stacking_model.pkl создан")

    # 6️⃣ (опционально) Тестирование на тестовом наборе
    if 'income' in test_data.columns:
        X_test = preprocessor.transform(test_data[numerical_features+categorical_features])
        y_test = test_data['income']
        score = stacking_model.score(X_test, y_test)
        print(f"ℹ️ R² на тестовом наборе: {score:.4f}")

if __name__ == "__main__":
    main()
