import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.impute import SimpleImputer
from scipy.sparse import issparse


train_data = pd.read_csv('../data/hackathon_income_train.csv', sep=';', on_bad_lines='skip')
test_data = pd.read_csv('../data/hackathon_income_test.csv', sep=';', on_bad_lines='skip')

numerical_features = ['age', 'turn_cur_cr_avg_v2', 'mob_cnt_days']
categorical_features = ['device_iphone_avg', 'vert_has_app_ru_tinkoff_investing']

available_numerical = [col for col in numerical_features if col in train_data.columns]
available_categorical = [col for col in categorical_features if col in train_data.columns]

if not available_numerical and not available_categorical:
    raise ValueError("Нет доступных признаков для предобработки!")

for col in available_numerical:
    train_data[col] = pd.to_numeric(train_data[col].astype(str).str.replace(',', '.'), errors='coerce')
    if col in test_data.columns:
        test_data[col] = pd.to_numeric(test_data[col].astype(str).str.replace(',', '.'), errors='coerce')

transformers = []
if available_numerical:
    transformers.append(('num', Pipeline([
('imputer', SimpleImputer(strategy='median')),
('scaler', StandardScaler())
]), available_numerical))
if available_categorical:
    transformers.append(('cat', Pipeline([
('imputer', SimpleImputer(strategy='most_frequent')),
('onehot', OneHotEncoder(handle_unknown='ignore'))
]), available_categorical))

preprocessor = ColumnTransformer(transformers)
joblib.dump(preprocessor, 'final_preprocessor.pkl')

possible_targets = ['income', 'Income', 'target', 'Target', 'incomeValue']
target_column = next((col for col in possible_targets if col in train_data.columns), None)
if target_column is None:
    raise ValueError("Не найден столбец с доходом.")

y_train = pd.to_numeric(train_data[target_column].astype(str).str.replace(',', '.'), errors='coerce')
mask = y_train.notna()
X_train_filtered = preprocessor.fit_transform(train_data.loc[mask, available_numerical + available_categorical])
y_train_filtered = y_train.loc[mask]

if issparse(X_train_filtered):
    X_train_array = X_train_filtered.toarray()
else:
    X_train_array = X_train_filtered

base_estimators = [
('rf', RandomForestRegressor(n_estimators=100, random_state=42)),
('gbr', GradientBoostingRegressor(n_estimators=100, random_state=42))
]

stacking_model = StackingRegressor(
estimators=base_estimators,
final_estimator=None,
passthrough=True
)
stacking_model.fit(X_train_array, y_train_filtered)
joblib.dump(stacking_model, 'final_stacking_model.pkl')

if target_column in test_data.columns:
    y_test = pd.to_numeric(test_data[target_column].astype(str).str.replace(',', '.'), errors='coerce')
    mask_test = y_test.notna()
    X_test = preprocessor.transform(test_data.loc[mask_test, available_numerical + available_categorical])
    if issparse(X_test):
        X_test = X_test.toarray()
        y_test_filtered = y_test.loc[mask_test]
        score = stacking_model.score(X_test, y_test_filtered)
        print(f"Точность на тесте: {score}")
