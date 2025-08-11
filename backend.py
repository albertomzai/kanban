"""
Backend server for Kanban application.
Implements CRUD endpoints for tasks stored in a JSON file.
"""

import json
import os
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS

# Path to the tasks data file. Can be overridden in tests via monkeypatch.
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

app = Flask(__name__, static_folder="static")
CORS(app)

# --------------------- Utility functions ---------------------

def _load_tasks():
    """Load tasks from the JSON file. Returns a list of task dicts."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # Ensure the file contains a list
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def _save_tasks(tasks):
    """Persist the tasks list to the JSON file."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

# --------------------- API routes ---------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = _load_tasks()
    return jsonify(tasks), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    content = data.get("content", "")
    if not content:
        abort(400, description="Content is required.")
    # Assign a new incremental ID
    tasks = _load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    task = {
        "id": new_id,
        "content": content,
        "status": data.get("status", "Por Hacer")
    }
    tasks.append(task)
    _save_tasks(tasks)
    return jsonify(task), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            # Update fields if present
            if "content" in data:
                task["content"] = data["content"]
            if "status" in data:
                task["status"] = data["status"]
            _save_tasks(tasks)
            return jsonify(task), 200
    abort(404, description="Task not found.")

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = _load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            # Remove the task and persist
            del tasks[i]
            _save_tasks(tasks)
            return '', 204
    abort(404, description="Task not found.")

# --------------------- Run server ---------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
