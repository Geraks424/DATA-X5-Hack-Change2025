"""
Скрипт проверки установки всех зависимостей
Проверяет, что все необходимые библиотеки установлены и работают
"""
import sys
import importlib

def check_module(module_name, package_name=None):
    """Проверка доступности модуля"""
    if package_name is None:
        package_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name} - НЕ УСТАНОВЛЕН")
        print(f"   Ошибка: {str(e)}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name} - ОШИБКА ПРИ ИМПОРТЕ")
        print(f"   Ошибка: {str(e)}")
        return False

def main():
    """Проверка всех зависимостей"""
    print("=" * 60)
    print("🔍 Проверка установки зависимостей AlphaWealth Neural")
    print("=" * 60)
    print()
    
    # Список зависимостей
    dependencies = [
        # Core
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
        
        # ML Models
        ("xgboost", "xgboost"),
        ("lightgbm", "lightgbm"),
        ("catboost", "catboost"),
        
        # Visualization
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("plotly", "plotly"),
        
        # Model Interpretation
        ("shap", "shap"),
        
        # Backend
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        
        # Frontend
        ("streamlit", "streamlit"),
        
        # Utilities
        ("yaml", "pyyaml"),
        ("joblib", "joblib"),
        ("scipy", "scipy"),
        ("requests", "requests"),
        ("dotenv", "python-dotenv"),
    ]
    
    print("📦 Проверка основных зависимостей:")
    print("-" * 60)
    
    results = []
    for module_name, package_name in dependencies:
        results.append(check_module(module_name, package_name))
    
    print()
    print("=" * 60)
    
    # Итоги
    installed = sum(results)
    total = len(results)
    
    if installed == total:
        print(f"✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ ({installed}/{total})")
        print()
        print("🎉 Отлично! Проект готов к использованию.")
        print()
        print("Следующие шаги:")
        print("1. Поместите данные в папку data/")
        print("2. Обучите модель: python train_model.py")
        print("3. Запустите приложение: python run_app.py")
        return 0
    else:
        print(f"❌ НЕКОТОРЫЕ ЗАВИСИМОСТИ ОТСУТСТВУЮТ ({installed}/{total})")
        print()
        print("⚠️  Установите недостающие зависимости:")
        print("   pip install -r requirements.txt")
        print()
        print("Или используйте скрипт установки:")
        print("   Windows: install.bat")
        print("   Linux/Mac: ./install.sh")
        return 1

if __name__ == "__main__":
    sys.exit(main())

