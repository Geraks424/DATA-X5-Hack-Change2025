"""
Script to train the income prediction model
Поддерживает как стандартные модели, так и AlphaWealth Neural ансамбль
"""
import argparse
import os
from src.model_trainer import ModelTrainer
from src.ensemble_trainer import EnsembleExpertCommittees
import yaml


def main():
    parser = argparse.ArgumentParser(description='Train income prediction model')
    parser.add_argument('--data', type=str, default='data/train.csv',
                       help='Path to training data')
    parser.add_argument('--model-type', type=str, default='alpha_wealth',
                       choices=['xgboost', 'lightgbm', 'catboost', 'alpha_wealth'],
                       help='Type of model to train (alpha_wealth = ensemble)')
    parser.add_argument('--output', type=str, default='models/income_model.pkl',
                       help='Output path for trained model')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧬 ALPHAWEALTH NEURAL - Обучение модели")
    print("=" * 60)
    print(f"Данные: {args.data}")
    print(f"Тип модели: {args.model_type}")
    print(f"Выходной файл: {args.output}")
    print("=" * 60)
    
    if args.model_type == 'alpha_wealth':
        # Обучение гибридного ансамбля AlphaWealth Neural
        print("\n🌟 Используется AlphaWealth Neural (гибридный ансамбль)")
        ensemble = EnsembleExpertCommittees(config_path=args.config)
        # Автоматическое определение целевой переменной
        from src.data_processing import DataProcessor
        processor = DataProcessor(args.config)
        train_df = processor.load_data(args.data)
        target_col = processor.detect_target_column(train_df) or 'income'
        print(f"   Целевая переменная: {target_col}")
        ensemble.train_ensemble(train_path=args.data, target_col=target_col)
        ensemble.save_ensemble(args.output)
        print(f"\n✅ Модель AlphaWealth Neural сохранена: {args.output}")
    else:
        # Обучение стандартной модели
        print(f"\n📊 Используется стандартная модель: {args.model_type}")
        trainer = ModelTrainer(config_path=args.config)
        # Автоматическое определение целевой переменной
        trainer.train_model(train_path=args.data, model_type=args.model_type, target_col=None)
        trainer.save_model(args.output)
        
        # Show feature importance
        print("\n📈 Top 20 Feature Importances:")
        importance_df = trainer.get_feature_importance(top_n=20)
        print(importance_df.to_string(index=False))
    
    print("\n🎉 Обучение завершено успешно!")


if __name__ == "__main__":
    main()

