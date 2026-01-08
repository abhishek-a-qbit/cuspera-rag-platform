import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Zero-deps API working!", "status": "success", "port": os.getenv("PORT", "8000")}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "healthy", "service": "Zero-deps API", "port": os.getenv("PORT", "8000")}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting zero-deps server on port {port}")
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()
