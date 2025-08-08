#!/usr/bin/env python3
"""
Flask backend for a Mini‑Trello Kanban board.
Implements CRUD operations over tasks stored in a JSON file.
All responses use the schema defined in the api_contract.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "tasks.json"
STATIC_FOLDER = BASE_DIR / "static"
TEMPLATE_FOLDER = BASE_DIR / "templates"

ALLOWED_STATES = {"Por Hacer", "En Progreso", "Hecho"}
DEFAULT_STATE = "Por Hacer"

# ---------------------------------------------------------------------------
# Flask app initialization
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=str(STATIC_FOLDER), template_folder=str(TEMPLATE_FOLDER))
CORS(app)  # Allow all origins (frontend served from the same host)

# ---------------------------------------------------------------------------
# Utility functions for task persistence
# ---------------------------------------------------------------------------
def _load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from TASKS_FILE. Return an empty list if file missing.

    Returns a list of dicts with keys: id (int), content (str), state (str).
    """
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # First run – start with an empty list
        return []
    except json.JSONDecodeError as exc:
        app.logger.error("Invalid JSON in %s: %s", TASKS_FILE, exc)
        abort(500, description="Corrupt tasks file")


def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Persist the given task list to TASKS_FILE.
    The file is written atomically by writing to a temp file first.
    """
    tmp_file = TASKS_FILE.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
    os.replace(tmp_file, TASKS_FILE)

# ---------------------------------------------------------------------------
# Helper for ID generation
# ---------------------------------------------------------------------------
def _next_id(tasks: List[Dict[str, Any]]) -> int:
    """Return the next incremental id based on existing tasks."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as a JSON list."""
    tasks = _load_tasks()
    return jsonify(tasks), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task.

    Expected JSON body: {"content": str, "state": str (optional)}.
    The state defaults to 'Por Hacer' if omitted.
    Returns the created task with its assigned id.
    """
    data = request.get_json(silent=True)
    if not data or "content" not in data:
        abort(400, description="Missing required field: content")

    content = str(data["content"]).strip()
    state = str(data.get("state", DEFAULT_STATE)).strip()
    if state not in ALLOWED_STATES:
        abort(400, description=f"Invalid state. Allowed: {', '.join(ALLOWED_STATES)}")

    tasks = _load_tasks()
    new_task = {
        "id": _next_id(tasks),
        "content": content,
        "state": state,
    }
    tasks.append(new_task)
    _save_tasks(tasks)
    return jsonify(new_task), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update content and/or state of an existing task.

    JSON body may contain "content" and/or "state". Both are optional but at least one must be present.
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, description="No data provided for update")

    tasks = _load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        abort(404, description=f"Task with id {task_id} not found")

    updated = False
    if "content" in data:
        content = str(data["content"]).strip()
        if not content:
            abort(400, description="Content cannot be empty")
        task["content"] = content
        updated = True
    if "state" in data:
        state = str(data["state"]).strip()
        if state not in ALLOWED_STATES:
            abort(400, description=f"Invalid state. Allowed: {', '.join(ALLOWED_STATES)}")
        task["state"] = state
        updated = True
    if not updated:
        abort(400, description="No valid fields to update")

    _save_tasks(tasks)
    return jsonify(task), 200

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete the task identified by task_id."""
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        abort(404, description=f"Task with id {task_id} not found")

    _save_tasks(new_tasks)
    return jsonify({"message": f"Task {task_id} deleted"}), 200

# ---------------------------------------------------------------------------
# Frontend serving route (root)
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the static index.html file."""
    return send_from_directory(app.static_folder, "index.html")

# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    response = jsonify({"error": error.description if hasattr(error, 'description') else str(error)})
    response.status_code = 400
    return response

@app.errorhandler(404)
def not_found(error):
    response = jsonify({"error": error.description if hasattr(error, 'description') else "Not found"})
    response.status_code = 404
    return response

@app.errorhandler(500)
def internal_error(error):
    response = jsonify({"error": "Internal server error"})
    response.status_code = 500
    return response

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
