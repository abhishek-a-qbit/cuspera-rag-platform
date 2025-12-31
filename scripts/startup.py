#!/usr/bin/env python3
"""
Cuspera System - Complete Startup Script
Initializes and tests the entire RAG platform
"""

import sys
import time
import subprocess
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Set up path for new folder structure
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Load environment
load_dotenv()

class CuspAutoSetup:
    def __init__(self):
        self.root = Path(__file__).parent.parent  # Go up to project root
        self.api_running = False
        self.api_process = None
    
    def check_requirements(self):
        """Verify all required files exist."""
        print("\n" + "="*60)
        print("STEP 1: Checking Requirements")
        print("="*60)
        
        required_files = [
            "config.py",
            "data_loader.py",
            "vector_store.py",
            "rag_graph.py",
            "api_backend.py",
            "frontend_integration.py"
        ]
        
        missing = []
        for f in required_files:
            path = self.root / f
            if path.exists():
                print(f"✓ {f}")
            else:
                print(f"✗ {f} - MISSING")
                missing.append(f)
        
        if missing:
            print(f"\n❌ Missing files: {missing}")
            return False
        
        print("\n✓ All required files present")
        return True
    
    def check_environment(self):
        """Verify environment variables."""
        print("\n" + "="*60)
        print("STEP 2: Checking Environment")
        print("="*60)
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and api_key != "your_gemini_api_key_here":
            print(f"✓ GOOGLE_API_KEY configured")
            return True
        else:
            print("✗ GOOGLE_API_KEY not found or not configured")
            print("\nTo fix:")
            print("1. Copy .env.example to .env")
            print("2. Add your Gemini API key to .env")
            print("3. Get key from: https://makersuite.google.com/app/apikey")
            return False
    
    def check_database(self):
        """Verify database files exist."""
        print("\n" + "="*60)
        print("STEP 3: Checking Database")
        print("="*60)
        
        db_path = self.root / "Database"
        if not db_path.exists():
            print(f"✗ Database folder not found at {db_path}")
            return False
        
        json_files = list(db_path.glob("*.json"))
        print(f"✓ Database folder exists")
        print(f"✓ Found {len(json_files)} dataset files")
        
        if len(json_files) < 20:
            print(f"⚠ Expected ~23 datasets, found {len(json_files)}")
        
        return len(json_files) > 0
    
    def start_api(self):
        """Start the FastAPI backend."""
        print("\n" + "="*60)
        print("STEP 4: Starting FastAPI Backend")
        print("="*60)
        
        try:
            print("Launching api_backend.py on port 8000...")
            
            # Start API in background
            self.api_process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "api_backend:app", "--reload"],
                cwd=self.root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for API to be ready
            print("Waiting for API to initialize...")
            for i in range(30):
                try:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        print("✓ API is running on http://localhost:8000")
                        self.api_running = True
                        return True
                except:
                    time.sleep(1)
                    print(".", end="", flush=True)
            
            print("\n✗ API failed to start")
            return False
        
        except Exception as e:
            print(f"✗ Error starting API: {e}")
            return False
    
    def test_endpoints(self):
        """Test RAG endpoints."""
        print("\n" + "="*60)
        print("STEP 5: Testing Endpoints")
        print("="*60)
        
        if not self.api_running:
            print("⚠ Skipping endpoint tests (API not running)")
            return False
        
        endpoints = [
            ("GET", "/health", None, "Health Check"),
            ("GET", "/products", None, "List Products"),
            ("GET", "/stats", None, "System Stats"),
        ]
        
        for method, endpoint, data, name in endpoints:
            try:
                url = f"http://localhost:8000{endpoint}"
                if method == "GET":
                    resp = requests.get(url, timeout=5)
                else:
                    resp = requests.post(url, json=data, timeout=5)
                
                if resp.status_code == 200:
                    print(f"✓ {name}")
                else:
                    print(f"✗ {name} (HTTP {resp.status_code})")
            except Exception as e:
                print(f"✗ {name}: {str(e)[:50]}")
        
        # Test RAG query
        print("\nTesting RAG endpoints...")
        try:
            resp = requests.post(
                "http://localhost:8000/query",
                json={"question": "What are the key features?", "top_k": 3},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                print(f"✓ Query endpoint (retrieved {data.get('context', {}).get('documents_retrieved', 0)} docs)")
            else:
                print(f"✗ Query endpoint (HTTP {resp.status_code})")
        except Exception as e:
            print(f"✗ Query endpoint: {str(e)[:50]}")
    
    def display_next_steps(self):
        """Display next steps for user."""
        print("\n" + "="*60)
        print("SETUP COMPLETE!")
        print("="*60)
        
        if self.api_running:
            print("\n✓ API is running at http://localhost:8000")
            print("\nYour RAG system is ready!")
        else:
            print("\n⚠ API is not running. Start it manually with:")
            print("   python api_backend.py")
        
        print("\n" + "="*60)
        print("NEXT STEPS")
        print("="*60)
        
        print("""
1. Frontend Integrations Ready:
   - Chat Interface (cusp_consultant.html)
   - Analytics UI (cuspera_analytics.txt)
   - Agent Reports (cuspera_agent.txt)

2. Test the system:
   python frontend_integration.py

3. API Documentation:
   http://localhost:8000/docs

4. To see your data:
   http://localhost:8000/products
   http://localhost:8000/stats

5. Try a query:
   curl -X POST http://localhost:8000/query \\
     -H "Content-Type: application/json" \\
     -d '{"question": "What are the key capabilities?", "top_k": 3}'

6. Connect your React UIs to the API endpoints

7. When ready, scale to multiple products!
""")
    
    def cleanup(self):
        """Cleanup on exit."""
        if self.api_process:
            print("\nShutting down API...")
            self.api_process.terminate()
            self.api_process.wait()
    
    def run(self):
        """Run complete setup."""
        try:
            print("\n" + "🚀 "*30)
            print("CUSPERA RAG PLATFORM - COMPLETE SETUP")
            print("🚀 "*30)
            
            # Checks
            if not self.check_requirements():
                return False
            
            if not self.check_environment():
                return False
            
            if not self.check_database():
                return False
            
            # Start API
            if not self.start_api():
                return False
            
            # Test
            time.sleep(2)
            self.test_endpoints()
            
            # Next steps
            self.display_next_steps()
            
            # Keep API running
            print("\n💡 Press Ctrl+C to stop the API...")
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\nShutdown requested...")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.cleanup()


if __name__ == "__main__":
    setup = CuspAutoSetup()
    setup.run()
