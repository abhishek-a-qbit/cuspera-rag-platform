#!/usr/bin/env python3
"""
Cuspera POC Quick Start - All in one
Starts both API and Streamlit app
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def main():
    root = Path(__file__).parent
    
    print("\n" + "="*70)
    print("🚀 CUSPERA RAG - POC QUICK START")
    print("="*70)
    
    # Check environment
    print("\n[1/3] Checking environment...")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ GOOGLE_API_KEY not configured")
        print("   1. Edit .env and add your API key")
        print("   2. Get key from: https://makersuite.google.com/app/apikey")
        return
    print("✓ Environment configured")
    
    # Start API
    print("\n[2/3] Starting FastAPI backend...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api_backend:app", "--reload"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for API
    print("   Waiting for API to start...")
    for i in range(30):
        try:
            import requests
            resp = requests.get("http://localhost:8000/health", timeout=2)
            if resp.status_code == 200:
                print("✓ API is running (http://localhost:8000)")
                break
        except:
            time.sleep(1)
            print(".", end="", flush=True)
    else:
        print("\n❌ API failed to start")
        return
    
    # Start Streamlit
    print("\n[3/3] Starting Streamlit app...")
    print("   Opening in browser (http://localhost:8501)...\n")
    
    time.sleep(2)  # Give API time to fully initialize
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd=root
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutdown complete")
    except Exception as e:
        print(f"\n❌ Error: {e}")
