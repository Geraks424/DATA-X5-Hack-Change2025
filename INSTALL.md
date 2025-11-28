# 📦 Инструкция по установке

Полная инструкция по установке всех зависимостей проекта AlphaWealth Neural на любом компьютере.

## 🎯 Требования

- **Python 3.9** или выше (рекомендуется 3.10+)
- **pip** (обычно идет вместе с Python)
- **Интернет-соединение** (для скачивания библиотек)

## 🚀 Быстрая установка

### Windows

1. **Откройте командную строку** (Win+R → `cmd` → Enter)
2. **Перейдите в папку проекта:**
   ```cmd
   cd путь\к\проекту\DATA-X5-Hack-Change2025
   ```
3. **Запустите скрипт установки:**
   ```cmd
   install.bat
   ```

### Linux / Mac

1. **Откройте терминал**
2. **Перейдите в папку проекта:**
   ```bash
   cd путь/к/проекту/DATA-X5-Hack-Change2025
   ```
3. **Сделайте скрипт исполняемым и запустите:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## 📋 Ручная установка

Если автоматические скрипты не работают, установите вручную:

### 1. Проверьте версию Python

```bash
python --version
# или
python3 --version
```

Должна быть версия **3.9** или выше.

### 2. Обновите pip

```bash
python -m pip install --upgrade pip
# или
python3 -m pip install --upgrade pip
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
# или
pip3 install -r requirements.txt
```

Если возникают ошибки прав доступа, используйте:

```bash
pip install --user -r requirements.txt
```

## 🔍 Что устанавливается

### Основные библиотеки:

- **pandas** - работа с данными
- **numpy** - численные вычисления
- **scikit-learn** - машинное обучение

### ML модели:

- **xgboost** - градиентный бустинг
- **lightgbm** - быстрый градиентный бустинг
- **catboost** - градиентный бустинг с категориями

### Визуализация:

- **matplotlib** - базовые графики
- **seaborn** - статистические графики
- **plotly** - интерактивные графики

### Backend:

- **fastapi** - веб-фреймворк
- **uvicorn** - ASGI сервер
- **pydantic** - валидация данных

### Frontend:

- **streamlit** - веб-интерфейс

### Дополнительные:

- **shap** - объяснимость моделей
- **requests** - HTTP запросы
- **pyyaml** - работа с конфигами
- **joblib** - сохранение моделей

## ✅ Проверка установки

После установки проверьте, что все работает:

```bash
python -c "import pandas, numpy, sklearn, xgboost, lightgbm, catboost, fastapi, streamlit; print('✅ Все библиотеки установлены!')"
```

Или запустите скрипт проверки:

```bash
python check_installation.py
```

## 🐛 Решение проблем

### Проблема: "Python не найден"

**Решение:**
1. Убедитесь, что Python установлен
2. Добавьте Python в PATH переменную окружения
3. Попробуйте использовать `python3` вместо `python`

### Проблема: "Permission denied" при установке

**Решение:**
```bash
pip install --user -r requirements.txt
```

Или используйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Проблема: Ошибки при установке некоторых библиотек

**Решение для Windows:**
- Установите [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Или используйте предкомпилированные версии

**Решение для Linux:**
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev
```

### Проблема: Медленная установка

**Решение:**
- Используйте зеркало PyPI в Китае (если в России):
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 🌐 Установка через setup.py

Альтернативный способ (установка как пакет):

```bash
pip install -e .
```

Это установит проект в "editable" режиме.

## 📦 Использование виртуального окружения (рекомендуется)

### Создание виртуального окружения:

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Деактивация:

```bash
deactivate
```

## 🔄 Обновление зависимостей

Если нужно обновить все библиотеки:

```bash
pip install --upgrade -r requirements.txt
```

## 📝 Следующие шаги

После успешной установки:

1. **Подготовьте данные:**
   - Поместите `train.csv` в папку `data/`
   - Поместите `test.csv` в папку `data/`

2. **Обучите модель:**
   ```bash
   python train_model.py --data data/train.csv
   ```

3. **Запустите приложение:**
   ```bash
   python run_app.py
   ```

## 💡 Полезные команды

- Проверить установленные пакеты: `pip list`
- Проверить конкретный пакет: `pip show pandas`
- Удалить пакет: `pip uninstall package_name`
- Экспортировать текущие зависимости: `pip freeze > requirements.txt`

---

*Если возникли проблемы, проверьте раздел "Решение проблем" выше или создайте issue в репозитории.*

