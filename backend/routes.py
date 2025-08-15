import json
import os

from flask import Blueprint, request, jsonify, abort

# Path to the tasks file in the project root
TASKS_FILE = os.path.join(os.getcwd(), "tasks.json")

api_bp = Blueprint("api", __name__)

def _load_tasks():
    """Load tasks from the JSON file. Return an empty list if file does not exist."""
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def _save_tasks(tasks):
    """Persist the given list of tasks to disk."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@api_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = _load_tasks()
    return jsonify(tasks), 200

@api_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    content = data.get("content")
    if not content:
        abort(400, description="'content' field is required")

    tasks = _load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": new_id, "content": content, "state": "Por Hacer"}
    tasks.append(task)
    _save_tasks(tasks)

    return jsonify(task), 201

@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = _load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            # Update content if provided
            if "content" in data:
                task["content"] = data["content"]
            # Update state if provided
            if "state" in data:
                task["state"] = data["state"]
            _save_tasks(tasks)
            return jsonify(task), 200

    abort(404, description="Task not found")

@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        abort(404, description="Task not found")

    _save_tasks(new_tasks)
    return jsonify({"message": "Deleted successfully"}), 200