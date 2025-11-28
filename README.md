# 🧬 AlphaWealth Neural - Alfa-Bank Income Prediction Solution

Полнофункциональное AI-решение с креативной моделью **AlphaWealth Neural v2.0** для прогнозирования дохода клиентов и формирования персональных рекомендаций по финансовым продуктам для Альфа-Банка.

**Философия:** Доход — это не просто цифра, а отражение финансовой ДНК клиента ✨

## 🎯 Описание проекта

Решение включает:
- **ML-модель** для точного предсказания дохода клиентов (метрика WMAE)
- **Backend API** (FastAPI) для получения предсказаний и объяснений
- **Web-интерфейс** (Streamlit) для визуализации и работы с моделью
- **Систему рекомендаций** финансовых продуктов на основе прогноза
- **SHAP-объяснения** для интерпретации предсказаний
- **Мониторинг качества** модели в реальном времени

## 📋 Требования

- **Python 3.9+** (рекомендуется 3.10+)
- **pip** (обычно идет вместе с Python)
- **Интернет-соединение** (для скачивания библиотек)

## 🚀 Быстрый старт

### 1. Автоматическая установка зависимостей

**Windows:**
```cmd
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Ручная установка

```bash
pip install -r requirements.txt
```

### 2. Проверка установки

```bash
python check_installation.py
```

Должно вывести: `✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ`

### 2. Подготовка данных

Поместите файлы данных в директорию `data/`:
- `data/train.csv` - обучающая выборка (должна содержать столбец `income`)
- `data/test.csv` - тестовая выборка (для финальных предсказаний)

**Важно**: Если у вас нет данных, решение может работать с синтетическими данными для демонстрации функциональности.

### 3. Обучение модели

```bash
python train_model.py --data data/train.csv --output models/income_model.pkl
```

Опции:
- `--data` - путь к обучающим данным
- `--model-type` - тип модели (`xgboost`, `lightgbm`, `catboost`)
- `--output` - путь для сохранения модели
- `--config` - путь к конфигурационному файлу

### 4. Запуск Backend API

```bash
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен по адресу: http://localhost:8000

### 5. Запуск Web-интерфейса

В новом терминале:

```bash
streamlit run streamlit_app.py
```

Интерфейс будет доступен по адресу: http://localhost:8501

## 📁 Структура проекта

```
.
├── src/                          # Исходный код
│   ├── __init__.py
│   ├── data_processing.py       # Обработка данных и feature engineering
│   ├── model_trainer.py         # Обучение моделей
│   ├── predictor.py             # Предсказания
│   ├── product_recommender.py   # Рекомендации продуктов
│   ├── api.py                   # FastAPI backend
│   └── monitoring.py            # Мониторинг модели
├── data/                         # Данные
│   ├── train.csv
│   └── test.csv
├── models/                       # Обученные модели
│   └── income_model.pkl
├── logs/                         # Логи и метрики
│   └── metrics.json
├── notebooks/                    # Jupyter notebooks для анализа
├── train_model.py               # Скрипт обучения модели
├── streamlit_app.py             # Streamlit веб-интерфейс
├── config.yaml                  # Конфигурация
├── requirements.txt             # Зависимости
└── README.md                    # Документация
```

## 🔧 Основные возможности

### 1. Предсказание дохода
- Ввод данных клиента через веб-интерфейс
- Автоматическое предсказание дохода
- API для программного доступа

### 2. Объяснение предсказаний (SHAP)
- Визуализация вклада каждого признака
- Waterfall-диаграммы
- Текстовые объяснения

### 3. Рекомендации продуктов
- Автоматический подбор финансовых продуктов
- Приоритизация на основе прогноза
- Персонализированные условия

### 4. Клиентская база
- Пакетная обработка клиентов
- Визуализация результатов
- Экспорт данных

### 5. Мониторинг
- Метрики качества в реальном времени
- История предсказаний
- Отслеживание производительности

## 📊 API Endpoints

### Основные эндпоинты:

- `GET /` - Информация об API
- `GET /health` - Проверка работоспособности
- `POST /predict` - Предсказание дохода для одного клиента
- `POST /batch_predict` - Пакетное предсказание
- `POST /shap_explain` - SHAP-объяснение предсказания
- `GET /recommend/{income}` - Рекомендации продуктов по доходу
- `GET /feature_importance` - Важность признаков модели

### Пример использования API:

```python
import requests

# Предсказание дохода
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "data": {
            "age": 35,
            "employment_years": 5,
            "education": "higher",
            "city": "Moscow"
        }
    }
)

result = response.json()
print(f"Предсказанный доход: {result['predicted_income']:.2f} ₽")
print(f"Рекомендации: {result['recommendations']}")
```

## 🎨 Интерфейс

Веб-интерфейс включает 4 основных раздела:

1. **🔮 Предсказание дохода** - ввод данных клиента и получение прогноза
2. **👥 Клиентская база** - пакетная обработка и анализ
3. **📊 Аналитика модели** - важность признаков и статистика
4. **📈 Мониторинг** - метрики качества и производительности

## 📈 Метрики модели

Модель оптимизирована для минимизации **WMAE** (Weighted Mean Absolute Error):

```
WMAE = sum(|y_true - y_pred| * weight) / sum(weight)
```

Дополнительные метрики:
- MAE (Mean Absolute Error)
- R² (Coefficient of Determination)
- Feature Importance

## 💡 Бизнес-ценность решения

### Для банка:
1. **Точная оценка платежеспособности** - снижение рисков при выдаче кредитов
2. **Персонализация предложений** - повышение конверсии за счет релевантных продуктов
3. **Оптимизация условий** - установка оптимальных процентных ставок
4. **Соответствие требованиям ЦБ** - контроль кредитоспособности

### Для клиентов:
1. **Индивидуальные предложения** - продукты, соответствующие финансовым возможностям
2. **Справедливые условия** - кредиты на основе реальной платежеспособности
3. **Прозрачность** - понимание, почему предлагаются конкретные продукты

## 🔍 Примеры использования

### Обучение модели с XGBoost:
```bash
python train_model.py --data data/train.csv --model-type xgboost
```

### Обучение модели с LightGBM:
```bash
python train_model.py --data data/train.csv --model-type lightgbm
```

### Получение предсказаний для тестовой выборки:

**Используя скрипт (рекомендуется):**
```bash
python generate_submission.py --test-data data/test.csv --model models/income_model.pkl --output submission.csv
```

**Или программно:**
```python
from src.predictor import IncomePredictor
import pandas as pd

# Загрузка модели
predictor = IncomePredictor("models/income_model.pkl")

# Загрузка тестовых данных
test_data = pd.read_csv("data/test.csv")

# Предсказания
predictions = predictor.predict(test_data)

# Сохранение результатов
submission = pd.DataFrame({
    'id': test_data['id'],
    'income': predictions
})
submission.to_csv('submission.csv', index=False)
```

## 🛠️ Разработка

### Формат данных

Обучающие данные должны содержать:
- Целевая переменная: `income` (доход клиента)
- Признаки: числовые и категориальные характеристики клиента

Пример структуры:
```csv
id,age,employment_years,education,city,income
1,35,5,higher,Moscow,75000
2,42,12,higher,St. Petersburg,120000
```

### Настройка конфигурации

Редактируйте `config.yaml` для изменения:
- Параметров модели
- Финансовых продуктов
- Настроек API и фронтенда

## 📝 Лицензия

Проект создан для образовательных целей в рамках хакатона Changellenge >> и Alfa-Bank.

## 👥 Авторы

Решение разработано для DATA-X5-Hack-Change2025

## 🔗 Ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## ⚠️ Важные замечания

1. **Модель требует обучения** перед использованием API и веб-интерфейса
2. **Структура данных** должна соответствовать ожидаемому формату
3. **Для продакшена** рекомендуется добавить аутентификацию и валидацию данных
4. **Мониторинг** настроен на локальное хранение метрик в JSON

## 🚀 Деплой

### Локальный запуск (рекомендуется для демонстрации)

1. Установите зависимости
2. Обучите модель
3. Запустите API: `uvicorn src.api:app`
4. Запустите фронтенд: `streamlit run streamlit_app.py`

### Docker (опционально)

Создайте `Dockerfile` и `docker-compose.yml` для контейнеризации:

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./data:/app/data
  
  frontend:
    build: .
    command: streamlit run streamlit_app.py
    ports:
      - "8501:8501"
    depends_on:
      - api
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте, что все зависимости установлены
2. Убедитесь, что модель обучена
3. Проверьте формат данных
4. Просмотрите логи в консоли

---

**Удачи в решении! 🎉**
