"""
Main entry point for Render deployment.
Imports FastAPI app from src/api_backend.py
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Change working directory to src for imports
os.chdir(os.path.join(os.path.dirname(__file__), 'src'))

# Import the FastAPI app
from api_backend import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
