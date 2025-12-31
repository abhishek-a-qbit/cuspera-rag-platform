"""
Public forwarder that forwards requests to your local backend
"""

from flask import Flask, request, jsonify, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your local backend URL
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
        
        # Forward request to backend
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

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except:
        return "27.7.213.119"  # Fallback to the IP we found

if __name__ == "__main__":
    public_ip = get_public_ip()
    port = 5001
    
    print(f"🌐 Public IP: {public_ip}")
    print(f"🔗 Public URL: http://{public_ip}:{port}")
    print(f"📋 Use this URL in Streamlit Cloud")
    print(f"📡 Forwarding to: {BACKEND_URL}")
    print()
    print("🚀 Starting public forwarder...")
    
    app.run(host='0.0.0.0', port=port, debug=False)
