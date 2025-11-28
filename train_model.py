"""
Script to train the income prediction model
"""
import argparse
import os
from src.model_trainer import ModelTrainer
import yaml


def main():
    parser = argparse.ArgumentParser(description='Train income prediction model')
    parser.add_argument('--data', type=str, default='data/train.csv',
                       help='Path to training data')
    parser.add_argument('--model-type', type=str, default=None,
                       choices=['xgboost', 'lightgbm', 'catboost'],
                       help='Type of model to train')
    parser.add_argument('--output', type=str, default='models/income_model.pkl',
                       help='Output path for trained model')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Load config to get default model type if not specified
    if args.model_type is None:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        args.model_type = config['model']['type']
    
    print(f"Training {args.model_type} model...")
    print(f"Data: {args.data}")
    print(f"Output: {args.output}")
    
    # Initialize trainer
    trainer = ModelTrainer(config_path=args.config)
    
    # Train model
    trainer.train_model(train_path=args.data, model_type=args.model_type)
    
    # Save model
    trainer.save_model(args.output)
    
    # Show feature importance
    print("\nTop 20 Feature Importances:")
    importance_df = trainer.get_feature_importance(top_n=20)
    print(importance_df.to_string(index=False))
    
    print("\nTraining completed successfully!")


if __name__ == "__main__":
    main()

