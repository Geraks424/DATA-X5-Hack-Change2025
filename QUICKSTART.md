# 🚀 Быстрый старт

Пошаговая инструкция по запуску решения за 5 минут.

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Генерация примерных данных (если нет реальных данных)

```bash
python scripts/generate_sample_data.py --samples 1000
```

Это создаст файлы `data/train.csv` и `data/test.csv` для демонстрации.

## Шаг 3: Обучение модели

```bash
python train_model.py --data data/train.csv --output models/income_model.pkl
```

Модель будет сохранена в `models/income_model.pkl`.

## Шаг 4: Запуск приложения

### Вариант A: Запуск всего приложения одним скриптом

```bash
python run_app.py
```

Это запустит и API, и веб-интерфейс автоматически.

### Вариант B: Запуск по отдельности

**Терминал 1 - API:**
```bash
python run_api.py
```

**Терминал 2 - Веб-интерфейс:**
```bash
streamlit run streamlit_app.py
```

## Шаг 5: Использование

1. Откройте браузер: http://localhost:8501
2. Перейдите в раздел "🔮 Предсказание дохода"
3. Заполните форму с данными клиента
4. Получите предсказание и рекомендации!

## Доступ к API напрямую

API документация: http://localhost:8000/docs

Пример запроса:
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "age": 35,
         "employment_years": 5,
         "education": "higher",
         "city": "Moscow"
       }
     }'
```

## Структура данных

### Формат обучающих данных (train.csv):

```csv
id,age,employment_years,education,city,family_status,has_children,income
1,35,5,higher,Moscow,married,1,75000
2,42,12,higher,St. Petersburg,single,0,120000
```

### Формат тестовых данных (test.csv):

Те же поля, но БЕЗ столбца `income`.

## Возможные проблемы

### Проблема: "Model not loaded"
**Решение:** Убедитесь, что модель обучена и файл `models/income_model.pkl` существует.

### Проблема: "API недоступен"
**Решение:** 
1. Проверьте, что API запущен: `python run_api.py`
2. Проверьте порт в `config.yaml` (по умолчанию 8000)

### Проблема: "Module not found"
**Решение:** Установите зависимости: `pip install -r requirements.txt`

## Следующие шаги

1. Замените примерные данные на реальные
2. Настройте гиперпараметры модели в `config.yaml`
3. Добавьте свои финансовые продукты в `config.yaml`
4. Настройте мониторинг под ваши нужды

Удачи! 🎉

