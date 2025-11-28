"""
Script to run the complete application (API + Frontend)
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def check_model_exists():
    """Check if model file exists"""
    model_path = Path("models/income_model.pkl")
    if not model_path.exists():
        print("⚠️  WARNING: Model file not found!")
        print("   Please train the model first:")
        print("   python train_model.py --data data/train.csv")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

def main():
    print("=" * 60)
    print("🚀 Starting Alfa-Bank Income Prediction Application")
    print("=" * 60)
    
    # Check model
    check_model_exists()
    
    print("\n📡 Starting API server...")
    # Start API in background
    api_process = subprocess.Popen(
        [sys.executable, "run_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a bit for API to start
    time.sleep(3)
    
    print("✅ API server started")
    print("\n🌐 Starting web interface...")
    print("   Interface will be available at http://localhost:8501")
    print("   API will be available at http://localhost:8000")
    print("\n" + "=" * 60)
    
    try:
        # Start Streamlit (blocking)
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        api_process.terminate()
        api_process.wait()
        print("✅ Application stopped")

if __name__ == "__main__":
    main()

