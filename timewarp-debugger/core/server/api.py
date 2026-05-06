import http.server
import socketserver
import json
import subprocess
from core.storage.io import load_recording

class DebuggerAPIHandler(http.server.SimpleHTTPRequestHandler):
    recording_path = "recording.json"

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/events':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                events = load_recording(self.recording_path)
                self.wfile.write(json.dumps(events).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            code = data.get('code', '')
            
            temp_file = "temp_playground.py"
            with open(temp_file, "w") as f:
                f.write(code)
                
            try:
                subprocess.run(
                    ["python", "core/cli/main.py", "record", temp_file, "-o", self.recording_path], 
                    check=True, capture_output=True
                )
                
                events = load_recording(self.recording_path)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(events).encode())
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                err_msg = e.stderr.decode() if e.stderr else str(e)
                self.wfile.write(json.dumps({"error": f"Execution failed: {err_msg}"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_server(filepath, port=8000):
    DebuggerAPIHandler.recording_path = filepath
    with socketserver.TCPServer(("", port), DebuggerAPIHandler) as httpd:
        print(f"TimeWarp API running on http://localhost:{port}")
        print(f"Serving data from {filepath}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
