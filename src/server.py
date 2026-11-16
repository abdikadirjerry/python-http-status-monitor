import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from src.storage import load_services
from src.manager import add_service, delete_service, refresh_all_services
from src.analytics import calculate_metrics

class MonitorHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath: Path, content_type: str):
        if not filepath.exists():
            self.send_error(404, "File Not Found")
            return
        content = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_file(Path("templates/index.html"), "text/html; charset=utf-8")
        elif parsed.path == "/static/app.js":
            self._send_file(Path("templates/app.js"), "application/javascript; charset=utf-8")
        elif parsed.path == "/api/services":
            services = load_services()
            metrics = calculate_metrics(services)
            self._send_json({"services": services, "metrics": metrics})
        else:
            self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/services":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            created = add_service(body["name"], body["url"], body["category"])
            self._send_json(created, 201)
        elif parsed.path == "/api/refresh":
            updated = refresh_all_services()
            self._send_json({"services": updated, "metrics": calculate_metrics(updated)})
        else:
            self.send_error(404, "Endpoint Not Found")

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/services":
            qs = parse_qs(parsed.query)
            srv_id = qs.get("id", [""])[0]
            deleted = delete_service(srv_id)
            self._send_json({"deleted": deleted}, 200 if deleted else 404)
        else:
            self.send_error(404, "Endpoint Not Found")

def run(port: int = 8000):
    server = HTTPServer(("0.0.0.0", port), MonitorHandler)
    print(f"[*] PulseMonitor Web Server running at http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()