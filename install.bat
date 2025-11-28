@echo off
REM Скрипт автоматической установки всех зависимостей для Windows
REM AlphaWealth Neural Project

echo ========================================
echo AlphaWealth Neural - Установка зависимостей
echo ========================================
echo.

REM Проверка версии Python
echo [1/4] Проверка версии Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден! Пожалуйста, установите Python 3.9 или выше.
    echo Скачайте с https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Проверка pip
echo [2/4] Проверка pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] pip не найден! Устанавливаем pip...
    python -m ensurepip --upgrade
)
python -m pip --version
echo.

REM Обновление pip
echo [3/4] Обновление pip до последней версии...
python -m pip install --upgrade pip
echo.

REM Установка зависимостей
echo [4/4] Установка зависимостей из requirements.txt...
echo Это может занять несколько минут...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось установить некоторые зависимости.
    echo Попробуйте установить вручную: pip install -r requirements.txt
    pause
    exit /b 1
)
echo.

echo ========================================
echo Установка завершена успешно!
echo ========================================
echo.
echo Следующие шаги:
echo 1. Поместите данные в папку data/
echo 2. Обучите модель: python train_model.py
echo 3. Запустите приложение: python run_app.py
echo.
pause

