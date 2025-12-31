"""
Simple proxy server to expose local backend to the internet
"""

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Your local backend URL
BACKEND_URL = "http://192.168.1.8:8000"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    try:
        # Forward request to local backend
        url = f"{BACKEND_URL}/{path}"
        
        if request.method == 'GET':
            resp = requests.get(url, params=request.args)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.json, params=request.args)
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.json, params=request.args)
        elif request.method == 'DELETE':
            resp = requests.delete(url, params=request.args)
        
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def proxy_root():
    try:
        resp = requests.get(BACKEND_URL)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting proxy server...")
    print(f"Forwarding to: {BACKEND_URL}")
    app.run(host='0.0.0.0', port=5000, debug=True)
