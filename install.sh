#!/bin/bash
# Скрипт автоматической установки всех зависимостей для Linux/Mac
# AlphaWealth Neural Project

set -e  # Остановка при ошибке

echo "========================================"
echo "AlphaWealth Neural - Установка зависимостей"
echo "========================================"
echo ""

# Проверка версии Python
echo "[1/4] Проверка версии Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python 3 не найден! Пожалуйста, установите Python 3.9 или выше."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Найдена версия: $PYTHON_VERSION"
echo ""

# Проверка версии (должна быть >= 3.9)
MIN_VERSION="3.9"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "[ОШИБКА] Требуется Python 3.9 или выше. Найдена версия: $PYTHON_VERSION"
    exit 1
fi

# Проверка pip
echo "[2/4] Проверка pip..."
if ! command -v pip3 &> /dev/null; then
    echo "[ОШИБКА] pip не найден! Устанавливаем pip..."
    python3 -m ensurepip --upgrade
fi
python3 -m pip --version
echo ""

# Обновление pip
echo "[3/4] Обновление pip до последней версии..."
python3 -m pip install --upgrade pip --user
echo ""

# Установка зависимостей
echo "[4/4] Установка зависимостей из requirements.txt..."
echo "Это может занять несколько минут..."
python3 -m pip install --user -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ОШИБКА] Не удалось установить некоторые зависимости."
    echo "Попробуйте установить вручную: pip3 install -r requirements.txt"
    exit 1
fi
echo ""

echo "========================================"
echo "Установка завершена успешно!"
echo "========================================"
echo ""
echo "Следующие шаги:"
echo "1. Поместите данные в папку data/"
echo "2. Обучите модель: python3 train_model.py"
echo "3. Запустите приложение: python3 run_app.py"
echo ""

