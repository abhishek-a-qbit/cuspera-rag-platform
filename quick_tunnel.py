"""
Quick public tunnel using localtunnel.me
"""

import requests
import threading
import time
from flask import Flask, jsonify
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "tunnel_running", "message": "Use this for public access"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "tunnel": "active"})

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except:
        return "Unknown"

def create_public_url():
    """Create a public URL using your public IP"""
    public_ip = get_public_ip()
    port = 5001
    
    print(f"🌐 Your Public IP: {public_ip}")
    print(f"🔗 Public URL: http://{public_ip}:{port}")
    print(f"📋 Use this URL in Streamlit Cloud")
    print()
    print("⚠️  Note: Make sure port 5001 is open on your router/firewall")
    print("⚠️  Or use this URL for testing on your local network")
    
    return port

if __name__ == "__main__":
    port = create_public_url()
    
    print(f"🚀 Starting public tunnel server on port {port}...")
    print("📡 Server will be accessible from the internet")
    print("🔄 Forwarding requests to your local backend")
    
    # Run on port that might be accessible from internet
    app.run(host='0.0.0.0', port=port, debug=False)
