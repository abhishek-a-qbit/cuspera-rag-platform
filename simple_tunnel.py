"""
Simple tunnel using Flask to expose local backend
"""

from flask import Flask, request, jsonify, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
            resp = requests.get(url, params=request.args, headers=headers)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.json, params=request.args, headers=headers)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.json, params=request.args, headers=headers)
        elif request.method == 'DELETE':
            resp = requests.delete(url, params=request.args, headers=headers)
        
        # Return response
        return Response(resp.content, resp.status_code, dict(resp.headers))
    except Exception as e:
        return jsonify({"error": str(e), "backend_url": BACKEND_URL}), 500

if __name__ == "__main__":
    print("🚀 Starting tunnel server...")
    print(f"📡 Forwarding to: {BACKEND_URL}")
    print("🌐 Tunnel will be available on port 5000")
    print("📋 Use this URL for Streamlit Cloud: http://YOUR_IP:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
