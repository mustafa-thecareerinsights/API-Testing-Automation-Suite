"""
Sample REST API for API Testing Automation Suite
Prepared by: Ruknuddin Asrari
Role: Software Quality Engineer
Organization: The Career Insights Hub LLC

This API uses only Python standard library modules so the test suite is easy
for reviewers to run without database or framework setup.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json

HOST = "127.0.0.1"
PORT = 5060

INITIAL_TASKS = {
    1: {"id": 1, "title": "Validate login API", "status": "open", "priority": "high"},
    2: {"id": 2, "title": "Verify student registration API", "status": "in_progress", "priority": "medium"},
}

tasks = {key: value.copy() for key, value in INITIAL_TASKS.items()}
next_id = 3

VALID_STATUSES = {"open", "in_progress", "resolved", "closed"}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}


def reset_data():
    global tasks, next_id
    tasks = {key: value.copy() for key, value in INITIAL_TASKS.items()}
    next_id = 3


class TaskAPIHandler(BaseHTTPRequestHandler):
    server_version = "TaskAPI/1.0"

    def _send_json(self, status_code, payload):
        response = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return None
        raw_body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return None

    def _error(self, message, status_code):
        self._send_json(status_code, {"success": False, "error": message})

    def _task_id_from_path(self, parsed_path):
        parts = parsed_path.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "tasks":
            try:
                return int(parts[1])
            except ValueError:
                return None
        return None

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            self._send_json(200, {
                "success": True,
                "service": "API Testing Automation Suite Sample API",
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            })
            return

        if parsed.path == "/tasks":
            query = parse_qs(parsed.query)
            status_filter = query.get("status", [None])[0]
            results = list(tasks.values())
            if status_filter:
                results = [task for task in results if task["status"] == status_filter]
            self._send_json(200, {"success": True, "count": len(results), "data": results})
            return

        task_id = self._task_id_from_path(parsed)
        if task_id is not None:
            task = tasks.get(task_id)
            if not task:
                self._error("Task not found", 404)
                return
            self._send_json(200, {"success": True, "data": task})
            return

        self._error("Endpoint not found", 404)

    def do_POST(self):
        global next_id
        parsed = urlparse(self.path)

        if parsed.path == "/reset":
            reset_data()
            self._send_json(200, {"success": True, "message": "Test data reset"})
            return

        if parsed.path == "/tasks":
            payload = self._read_json()
            if not payload:
                self._error("Request body must be valid JSON", 400)
                return

            title = str(payload.get("title", "")).strip()
            status = payload.get("status", "open")
            priority = payload.get("priority", "medium")

            if not title:
                self._error("title is required", 400)
                return
            if status not in VALID_STATUSES:
                self._error("invalid status", 400)
                return
            if priority not in VALID_PRIORITIES:
                self._error("invalid priority", 400)
                return

            task = {"id": next_id, "title": title, "status": status, "priority": priority}
            tasks[next_id] = task
            next_id += 1
            self._send_json(201, {"success": True, "data": task})
            return

        self._error("Endpoint not found", 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        task_id = self._task_id_from_path(parsed)
        if task_id is None:
            self._error("Endpoint not found", 404)
            return

        task = tasks.get(task_id)
        if not task:
            self._error("Task not found", 404)
            return

        payload = self._read_json()
        if not payload:
            self._error("Request body must be valid JSON", 400)
            return

        if "title" in payload:
            title = str(payload["title"]).strip()
            if not title:
                self._error("title cannot be empty", 400)
                return
            task["title"] = title

        if "status" in payload:
            if payload["status"] not in VALID_STATUSES:
                self._error("invalid status", 400)
                return
            task["status"] = payload["status"]

        if "priority" in payload:
            if payload["priority"] not in VALID_PRIORITIES:
                self._error("invalid priority", 400)
                return
            task["priority"] = payload["priority"]

        self._send_json(200, {"success": True, "data": task})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        task_id = self._task_id_from_path(parsed)
        if task_id is None:
            self._error("Endpoint not found", 404)
            return

        task = tasks.pop(task_id, None)
        if not task:
            self._error("Task not found", 404)
            return
        self._send_json(200, {"success": True, "deleted_id": task_id})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), TaskAPIHandler)
    print(f"API server running at http://{HOST}:{PORT}")
    server.serve_forever()
