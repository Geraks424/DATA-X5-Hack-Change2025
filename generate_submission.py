"""
Script to generate submission file for the hackathon platform
Поддерживает различные форматы данных (Income/income, Id/id)
"""
import argparse
import pandas as pd
from pathlib import Path
from src.predictor import IncomePredictor
from src.alpha_predictor import AlphaWealthPredictor
from src.data_processing import DataProcessor
import os


def main():
    parser = argparse.ArgumentParser(description='Generate submission file')
    parser.add_argument('--test-data', type=str, default='data/test.csv',
                       help='Path to test data')
    parser.add_argument('--model', type=str, default='models/income_model.pkl',
                       help='Path to trained model')
    parser.add_argument('--output', type=str, default='submission.csv',
                       help='Output submission file')
    
    args = parser.parse_args()
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"❌ Error: Model file not found: {args.model}")
        print("   Please train the model first:")
        print("   python train_model.py --data data/train.csv")
        return
    
    # Check if test data exists
    if not os.path.exists(args.test_data):
        print(f"❌ Error: Test data file not found: {args.test_data}")
        print("   Please provide test data or generate sample data:")
        print("   python scripts/generate_sample_data.py")
        return
    
    print(f"📊 Loading model from {args.model}...")
    try:
        # Пробуем загрузить как AlphaWealth, если не получится - стандартный
        try:
            predictor = AlphaWealthPredictor(args.model)
            print("   ✅ AlphaWealth Neural loaded")
        except:
            predictor = IncomePredictor(args.model)
            print("   ✅ Standard predictor loaded")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return
    
    print(f"📂 Loading test data from {args.test_data}...")
    processor = DataProcessor()
    try:
        test_data = processor.load_data(args.test_data)
        print(f"   Loaded {len(test_data)} samples")
        print(f"   Columns: {list(test_data.columns)[:5]}...")
    except Exception as e:
        print(f"❌ Error loading test data: {str(e)}")
        return
    
    # Определяем ID столбец (поддержка Id/id/ID)
    id_col = processor.detect_id_column(test_data)
    if id_col is None:
        print("⚠️  Warning: ID column not found. Using index as ID.")
        ids = pd.Series(range(1, len(test_data) + 1))
        id_col_name = "Id"
    else:
        ids = test_data[id_col].copy()
        id_col_name = id_col
        print(f"   ✅ ID column detected: {id_col}")
    
    # Удаляем ID столбец для предсказания
    drop_cols = [id_col] if id_col else []
    test_data_for_pred = test_data.drop(columns=drop_cols, errors='ignore')
    
    print("🔮 Generating predictions...")
    try:
        predictions = predictor.predict(test_data_for_pred)
        print(f"   ✅ Generated {len(predictions)} predictions")
        print(f"   Mean prediction: {predictions.mean():.2f} ₽")
        print(f"   Min prediction: {predictions.min():.2f} ₽")
        print(f"   Max prediction: {predictions.max():.2f} ₽")
    except Exception as e:
        print(f"❌ Error generating predictions: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Определяем формат submission (поддержка Income/income)
    # Проверяем, есть ли sample_submission для формата
    income_col_name = "Income"  # По умолчанию заглавная, как в примере
    
    # Create submission dataframe
    submission = pd.DataFrame({
        id_col_name: ids,
        income_col_name: predictions
    })
    
    # Ensure income is non-negative and reasonable
    submission[income_col_name] = submission[income_col_name].clip(lower=0)
    
    # Save submission
    print(f"💾 Saving submission to {args.output}...")
    submission.to_csv(args.output, index=False)
    
    print(f"✅ Submission file created successfully!")
    print(f"   File: {args.output}")
    print(f"   Shape: {submission.shape}")
    print(f"   Columns: {list(submission.columns)}")
    print(f"\n📋 First 5 predictions:")
    print(submission.head().to_string(index=False))
    
    print(f"\n🚀 Ready to submit! Upload {args.output} to the hackathon platform.")


if __name__ == "__main__":
    main()

