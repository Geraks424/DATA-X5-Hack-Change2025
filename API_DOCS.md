# 📚 API Документация

Документация по API эндпоинтам для AlphaWealth Neural.

## 🔗 Базовый URL

```
http://localhost:8000
```

## 📋 Эндпоинты

### 1. GET /api/clients

Получить список клиентов из `hackathon_income_test.csv`.

**Цель:** получить список клиентов из hackathon_income_test.csv

**Запрос:**
```
GET /api/clients
```

**Ответ (JSON):**
```json
[
  {
    "id": "0",
    "age": 34,
    "gender": "Мужской",
    "city": "Ижевск"
  },
  {
    "id": "1",
    "age": 45,
    "gender": "Женский",
    "city": "Саратов"
  }
]
```

**Поля:**
- **Обязательные:** `id`, `age`, `gender`
- **Опциональные:** `city`, `adminarea` и др. (если есть в данных)

**Пример запроса:**
```bash
curl http://localhost:8000/api/clients
```

---

### 2. POST /api/predict

Получить прогноз и объяснение для выбранного клиента.

**Цель:** получить прогноз и объяснение для выбранного клиента

**Запрос:**
```
POST /api/predict
Content-Type: application/json

{
  "client_id": "0"
}
```

**Ответ (JSON):**
```json
{
  "predicted_income": 85200,
  "shap_values": {
    "per_capita_income_rur_amt": 21000,
    "dda_rur_amt_cm_avg": 15000,
    "blacklist_flag": -12000,
    "loan_cnt": -8000,
    "age": 5000
  },
  "recommendations": [
    {
      "product": "Автокредит до 1.5 млн",
      "reason": "Стабильный доход и низкая долговая нагрузка"
    },
    {
      "product": "Премиальная дебетовая карта",
      "reason": "Активное использование мобильного банка"
    }
  ]
}
```

**Поля ответа:**
- `predicted_income` (float) - прогнозируемый доход в рублях
- `shap_values` (object) - значения SHAP для топ признаков (вклад в предсказание)
- `recommendations` (array) - список рекомендуемых продуктов с причинами

**Пример запроса:**
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"client_id": "0"}'
```

---

### 3. GET /health

Проверка работоспособности API и загрузки модели.

**Запрос:**
```
GET /health
```

**Ответ:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

### 4. POST /predict (Legacy)

Старый эндпоинт для предсказания с полными данными клиента (обратная совместимость).

**Запрос:**
```
POST /predict
Content-Type: application/json

{
  "data": {
    "age": 35,
    "employment_years": 5,
    "education": "higher",
    "city": "Moscow"
  }
}
```

---

### 5. GET /feature_importance

Получить важность признаков модели.

**Запрос:**
```
GET /feature_importance?top_n=20
```

**Ответ:**
```json
{
  "features": [
    {
      "feature": "age",
      "importance": 0.15
    },
    ...
  ]
}
```

---

## 🔧 Настройка

### Путь к test файлу

Убедитесь, что файл `hackathon_income_test.csv` находится в одном из следующих мест:
- `data/hackathon_income_test.csv`
- `hackathon_income_test.csv`
- Укажите путь в `config.yaml`:

```yaml
paths:
  hackathon_test_data: "data/hackathon_income_test.csv"
```

### Запуск API

```bash
python run_api.py
```

Или напрямую:

```bash
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

---

## 📝 Примеры использования

### Python

```python
import requests

# Получить список клиентов
clients = requests.get("http://localhost:8000/api/clients").json()
print(clients)

# Получить прогноз для клиента
prediction = requests.post(
    "http://localhost:8000/api/predict",
    json={"client_id": "0"}
).json()
print(f"Доход: {prediction['predicted_income']}")
print(f"SHAP: {prediction['shap_values']}")
print(f"Рекомендации: {prediction['recommendations']}")
```

### JavaScript (fetch)

```javascript
// Получить список клиентов
fetch('http://localhost:8000/api/clients')
  .then(response => response.json())
  .then(clients => console.log(clients));

// Получить прогноз
fetch('http://localhost:8000/api/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({client_id: '0'})
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## ⚠️ Ошибки

### 404 - Клиент не найден
```json
{
  "detail": "Client with id '999' not found"
}
```

### 503 - Модель не загружена
```json
{
  "detail": "Model not loaded. Please train the model first."
}
```

### 404 - Test данные не найдены
```json
{
  "detail": "Test data not loaded. Please ensure hackathon_income_test.csv is in data/ directory."
}
```

---

*Документация актуальна для версии API 1.0.0*

