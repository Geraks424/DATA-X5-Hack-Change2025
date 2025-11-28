"""
Setup script for AlphaWealth Neural project
Установка всех зависимостей проекта
"""
from setuptools import setup, find_packages
from pathlib import Path

# Читаем README для длинного описания
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')

# Читаем requirements.txt
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#') and not line.startswith('-')
    ]

setup(
    name="alphawealth-neural",
    version="2.0.0",
    author="Alfa-Bank Hackathon Team",
    description="AlphaWealth Neural - Креативная модель предсказания дохода клиентов",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/alphawealth-neural",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "alphawealth-train=train_model:main",
            "alphawealth-predict=generate_submission:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

