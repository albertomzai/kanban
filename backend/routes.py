"""API endpoints for task management."""

import json
from pathlib import Path
from flask import request, jsonify, abort, Blueprint

# Path to the tasks file in project root
TASKS_FILE = Path(__file__).resolve().parent.parent / "tasks.json"

api_bp = Blueprint("api", __name__, url_prefix="/api")

def _load_tasks() -> list[dict]:
    """Load tasks from the JSON file.

    Returns:
        List of task dictionaries.
    """
    try:
        if not TASKS_FILE.exists():
            return []
        with TASKS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_tasks(tasks: list[dict]) -> None:
    """Persist tasks to the JSON file."""
    with TASKS_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

@api_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks."""
    return jsonify(_load_tasks()), 200

@api_bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task.

    Expects JSON body with 'content'.
    The new task is assigned an incremental id and status 'Por Hacer'."""
    data = request.get_json() or {}
    content = data.get("content")

    if not content:
        abort(400, description="'content' field is required.")

    tasks = _load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "content": content, "status": "Por Hacer"}
    tasks.append(new_task)
    _save_tasks(tasks)

    return jsonify(new_task), 201

@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task.

    Accepts partial updates for 'content' and/or 'status'."""
    data = request.get_json() or {}

    tasks = _load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        abort(404, description="Task not found.")

    content = data.get("content")
    status = data.get("status")

    if content is not None:
        task["content"] = content
    if status is not None:
        task["status"] = status

    _save_tasks(tasks)
    return jsonify(task), 200

@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by its id."""
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        abort(404, description="Task not found.")

    _save_tasks(new_tasks)
    return jsonify({"message": "Task deleted."}), 200