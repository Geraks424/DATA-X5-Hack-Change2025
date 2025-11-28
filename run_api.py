"""
Script to run the FastAPI backend
"""
import uvicorn
import yaml
import sys

if __name__ == "__main__":
    # Load configuration
    try:
        with open("config.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        host = config['api']['host']
        port = config['api']['port']
    except:
        host = "0.0.0.0"
        port = 8000
    
    print(f"Starting API server on http://{host}:{port}")
    print(f"API docs available at http://{host}:{port}/docs")
    
    uvicorn.run(
        "src.api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

