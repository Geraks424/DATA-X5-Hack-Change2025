# Прогноз дохода клиента

## Команда проекта

**Команда:** DATA X5

### Участники

**Капитан --- Data Analyst** ФИО: Романенко Валерия Телеграм:
@val_romanenko Телефон: +79042590549 E-Mail: leraromanenko565@gmail.com
Город: Vladimir

**Backend-разработчик** ФИО: Досков Марк Телеграм: @Geraksksks Телефон:
+79021785626 E-Mail: markdoskoff@mail.ru Город: Irkutsk

**Data Analyst** ФИО: Черепко Полина Телеграм: @polinaeter Телефон:
+79304070809 E-Mail: cherpolinaa@mail.ru Город: Moscow

**Frontend-разработчик** ФИО: Зеленов Ярослав Телеграм: @My\|fxunter
Телефон: +79191332319 E-Mail: mobzila567@gmail.com Город: Moscow

**Data Analyst** ФИО: Логачева Полина Телеграм: @polina_logacheva
Телефон: +79037083108 E-Mail: logacheva.polina@gmail.com Город: Moscow

## Бизнес-постановка задачи

Разработать AI-решение для прогноза доходов клиентов и формирования
персональных рекомендаций по финансовым продуктам.

## Используемые данные

-   hackathon_income_train.csv
-   hackathon_income_test.csv

## Структура проекта

    project/
    ├─ backend/
    │   ├─ app.py
    │   ├─ model_utils.py
    │   └─ train_models.py
    ├─ frontend/
    │   ├─ index.html
    │   ├─ styles.css
    │   └─ script.js
    ├─ data/
    │   ├─ hackathon_income_train.csv
    │   └─ hackathon_income_test.csv
    ├─ README.md
    ├─ requirements.txt

## Особенности модели

### Финансовые архетипы клиентов

1.  ZOOMERS --- молодые, tech-savvy
2.  MILLENNIALS --- надежные профессионалы
3.  SMART SAVERS --- умные кредитчики
4.  ADVENTURER --- путешественники
5.  PROFESSIONALS --- финансовые эксперты

## Используемые библиотеки

-   pandas
-   numpy
-   scikit-learn
-   flask
-   joblib

## Установка окружения

1.  python -m venv venv
2.  Активировать окружение
3.  pip install pandas numpy scikit-learn flask joblib

## Генерация модели

    python backend/train_models.py

## Запуск API

    python backend/app.py

Эндпоинт /predict принимает JSON.

## Шаги запуска пайплайна

1.  Сохранение модели
2.  Запуск ML
3.  Запуск API
4.  Настройка backend
5.  Настройка frontend
6.  Сборка пайплайна
7.  Тестирование
