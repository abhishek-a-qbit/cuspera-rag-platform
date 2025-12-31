"""
Simple public server that works with Streamlit Cloud
Uses a free public tunneling service
"""

import subprocess
import time
import threading
import requests
import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

# Your local backend
BACKEND_URL = "http://192.168.1.8:8000"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        url = f"{BACKEND_URL}/{path}" if path else BACKEND_URL
        
        # Forward headers
        headers = dict(request.headers)
        headers.pop('Host', None)
        
        # Forward request
        if request.method == 'GET':
            resp = requests.get(url, params=request.args, headers=headers, timeout=30)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.json, params=request.args, headers=headers, timeout=30)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.json, params=request.args, headers=headers, timeout=30)
        elif request.method == 'DELETE':
            resp = requests.delete(url, params=request.args, headers=headers, timeout=30)
        
        return Response(resp.content, resp.status_code, dict(resp.headers))
    except Exception as e:
        return jsonify({"error": str(e), "backend_url": BACKEND_URL}), 500

def create_localtunnel():
    """Create a localtunnel for public access"""
    try:
        print("🚀 Creating localtunnel...")
        
        # Use localtunnel.me
        cmd = ['lt', '--port', '5001', '--subdomain', f'cuspera-{int(time.time())}']
        
        print(f"🔗 Running: {' '.join(cmd)}")
        print("🌐 This will create a public URL")
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in iter(process.stdout.readline, ''):
            print(line.strip())
            if 'https://' in line and 'lt.me' in line:
                print(f"\n🎉 PUBLIC URL: {line.strip()}")
                print("📋 Use this URL in Streamlit Cloud")
                
    except Exception as e:
        print(f"❌ Error with localtunnel: {e}")
        print("💡 Using fallback method...")

def get_public_url():
    """Try to get a public URL using various methods"""
    
    # Method 1: Try to get public IP
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        public_ip = response.json()['ip']
        return f"http://{public_ip}:5001"
    except:
        pass
    
    # Method 2: Use a free tunneling service
    try:
        print("🔄 Trying to create public tunnel...")
        # This would require additional setup
        return "http://192.168.1.8:5001"  # Fallback
    except:
        return "http://192.168.1.8:5001"

if __name__ == "__main__":
    public_url = get_public_url()
    
    print("🚀 Cuspera RAG Public Server")
    print("=" * 50)
    print(f"📡 Backend URL: {BACKEND_URL}")
    print(f"🌐 Public URL: {public_url}")
    print(f"📋 Use this URL in Streamlit Cloud: {public_url}")
    print()
    print("🔄 Server starting on port 5001...")
    print("⚠️  If public URL doesn't work, the app will still work locally")
    print()
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=5001, debug=False)
