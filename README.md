# Прогноз дохода клиента

Проект позволяет прогнозировать доход клиента банка на основе его финансового и цифрового поведения.

## Структура проекта

```
project/
├─ backend/
│   └─ app.py
├─ frontend/
│   ├─ index.html
│   ├─ style.css
│   └─ script.js
├─ data/
│   ├─ hackathon_income_train.csv
│   └─ hackathon_income_test.csv
└─ README.md
```

## Установка

1. Создать виртуальное окружение:

```bash
python -m venv venv
```

2. Активировать его:

- Windows: `venv\Scripts\activate`
- Linux/macOS: `source venv/bin/activate`

3. Установить зависимости:

```bash
pip install pandas numpy scikit-learn flask joblib
```

## Генерация моделей

```bash
python backend/train_models.py
```

## Запуск сервера

```bash
python backend/app.py
```

- Сервер доступен по адресу: `http://127.0.0.1:5000/`
- Эндпоинт `/predict` принимает POST-запрос с JSON:

```json
{
  "age": 30,
  "turn_cur_cr_avg_v2": 50000,
  "mob_cnt_days": 120,
  "device_iphone_avg": 1,
  "vert_has_app_ru_tinkoff_investing": 1
}
```

## Фронтенд

- Открыть `frontend/index.html` в браузере.
- Ввести данные и нажать кнопку **Прогнозировать доход**.
- Результат отображается на странице.

## Зависимости

- Python 3.8+
- pandas
- numpy
- scikit-learn
- flask
- joblib
