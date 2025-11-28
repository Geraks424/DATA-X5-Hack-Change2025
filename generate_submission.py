"""
Script to generate submission file for the hackathon platform
"""
import argparse
import pandas as pd
from pathlib import Path
from src.predictor import IncomePredictor
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
        predictor = IncomePredictor(args.model)
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return
    
    print(f"📂 Loading test data from {args.test_data}...")
    try:
        test_data = pd.read_csv(args.test_data)
        print(f"   Loaded {len(test_data)} samples")
    except Exception as e:
        print(f"❌ Error loading test data: {str(e)}")
        return
    
    # Check for ID column
    if 'id' not in test_data.columns:
        print("⚠️  Warning: 'id' column not found. Using index as ID.")
        test_data['id'] = test_data.index + 1
    
    # Get IDs before prediction
    ids = test_data['id'].copy()
    
    # Remove ID column for prediction (if it exists)
    test_data_for_pred = test_data.drop(columns=['id'], errors='ignore')
    
    print("🔮 Generating predictions...")
    try:
        predictions = predictor.predict(test_data_for_pred)
        print(f"   Generated {len(predictions)} predictions")
        print(f"   Mean prediction: {predictions.mean():.2f} ₽")
        print(f"   Min prediction: {predictions.min():.2f} ₽")
        print(f"   Max prediction: {predictions.max():.2f} ₽")
    except Exception as e:
        print(f"❌ Error generating predictions: {str(e)}")
        return
    
    # Create submission dataframe
    submission = pd.DataFrame({
        'id': ids,
        'income': predictions
    })
    
    # Ensure income is non-negative and reasonable
    submission['income'] = submission['income'].clip(lower=0)
    
    # Save submission
    print(f"💾 Saving submission to {args.output}...")
    submission.to_csv(args.output, index=False)
    
    print(f"✅ Submission file created successfully!")
    print(f"   File: {args.output}")
    print(f"   Shape: {submission.shape}")
    print(f"\n📋 First 5 predictions:")
    print(submission.head().to_string(index=False))
    
    print(f"\n🚀 Ready to submit! Upload {args.output} to the hackathon platform.")


if __name__ == "__main__":
    main()

