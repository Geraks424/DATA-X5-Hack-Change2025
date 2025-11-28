# 🚀 Руководство по развертыванию

Полное руководство по развертыванию проекта на новом компьютере.

## 📦 Подготовка к развертыванию

### Что нужно перед началом:

1. ✅ **Python 3.9+** установлен на компьютере
2. ✅ **Интернет-соединение** для скачивания библиотек
3. ✅ **Проект скопирован** на новый компьютер

## 🎯 Шаг за шагом

### Шаг 1: Копирование проекта

Скопируйте всю папку проекта на новый компьютер или клонируйте репозиторий:

```bash
git clone <repository-url>
cd DATA-X5-Hack-Change2025
```

### Шаг 2: Установка зависимостей

#### Вариант A: Автоматическая установка (рекомендуется)

**Windows:**
```cmd
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

#### Вариант B: Ручная установка

```bash
pip install -r requirements.txt
```

### Шаг 3: Проверка установки

```bash
python check_installation.py
```

Если все установлено правильно, увидите:
```
✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ (21/21)
```

### Шаг 4: Подготовка данных

Поместите файлы данных в папку `data/`:
- `data/train.csv` - обучающая выборка
- `data/test.csv` - тестовая выборка (опционально)

**Если данных нет**, можно сгенерировать примерные:
```bash
python scripts/generate_sample_data.py --samples 1000
```

### Шаг 5: Обучение модели

```bash
python train_model.py --data data/train.csv --model-type alpha_wealth
```

Модель будет сохранена в `models/income_model.pkl`

### Шаг 6: Запуск приложения

#### Полное приложение (API + Frontend):
```bash
python run_app.py
```

#### Или отдельно:

**API:**
```bash
python run_api.py
```

**Frontend:**
```bash
streamlit run streamlit_app.py
```

## 🔧 Использование виртуального окружения (рекомендуется)

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

## 🌐 Развертывание на сервере

### Использование Docker (если настроен):

```bash
docker-compose up -d
```

### Использование systemd (Linux):

Создайте файл `/etc/systemd/system/alphawealth-api.service`:

```ini
[Unit]
Description=AlphaWealth Neural API
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/DATA-X5-Hack-Change2025
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python run_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl enable alphawealth-api
sudo systemctl start alphawealth-api
```

## 📊 Проверка работоспособности

### Проверка API:

```bash
curl http://localhost:8000/health
```

Должен вернуть:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Проверка Frontend:

Откройте в браузере: `http://localhost:8501`

## 🔍 Устранение неполадок

### Проблема: "Module not found"

**Решение:**
```bash
pip install -r requirements.txt
```

### Проблема: "Permission denied"

**Решение:**
```bash
pip install --user -r requirements.txt
```

Или используйте виртуальное окружение.

### Проблема: Модель не найдена

**Решение:**
1. Убедитесь, что модель обучена: `python train_model.py`
2. Проверьте путь к модели в `config.yaml`
3. Убедитесь, что файл `models/income_model.pkl` существует

### Проблема: Порт занят

**Решение:**
Измените порты в `config.yaml`:
```yaml
api:
  port: 8001  # Измените на свободный порт

frontend:
  port: 8502  # Измените на свободный порт
```

## 📝 Файлы конфигурации

Основные файлы, которые могут потребовать настройки:

- `config.yaml` - общая конфигурация
- `requirements.txt` - зависимости Python
- `.env` - переменные окружения (если используется)

## ✅ Чеклист развертывания

- [ ] Python 3.9+ установлен
- [ ] Проект скопирован на компьютер
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Установка проверена (`python check_installation.py`)
- [ ] Данные подготовлены (или сгенерированы)
- [ ] Модель обучена (`python train_model.py`)
- [ ] API запущен и проверен
- [ ] Frontend запущен и доступен

## 🎉 Готово!

После выполнения всех шагов проект полностью готов к использованию на новом компьютере!

---

**Дополнительная информация:**
- [INSTALL.md](INSTALL.md) - Подробная инструкция по установке
- [QUICK_INSTALL.md](QUICK_INSTALL.md) - Быстрая установка
- [README.md](README.md) - Общая документация проекта

