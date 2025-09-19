"""Package initialization for the backend Flask application."""

import os
from flask import Flask, Blueprint, jsonify, request
from .tasks import load_tasks, save_tasks, get_next_id

# Blueprint for API routes
api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/tasks", methods=["GET"])
def get_all_tasks():
    """Return all tasks from the JSON store."""
    tasks = load_tasks()
    return jsonify(tasks), 200

@api_bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task with content and default state 'Por Hacer'."""
    data = request.get_json() or {}
    content = data.get("content")
    if not content:
        return jsonify({"error": "Content is required."}), 400

    tasks = load_tasks()
    new_id = get_next_id(tasks)
    new_task = {"id": new_id, "content": content, "state": "Por Hacer"}
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update content or state of an existing task."""
    data = request.get_json() or {}
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            # Update fields if provided
            if "content" in data:
                task["content"] = data["content"]
            if "state" in data:
                task["state"] = data["state"]
            save_tasks(tasks)
            return jsonify(task), 200

    return jsonify({"error": "Task not found."}), 404

@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by its ID."""
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Task not found."}), 404

    save_tasks(new_tasks)
    return jsonify({"message": f"Task {task_id} deleted."}), 200

def create_app():
    """Factory to create and configure the Flask application."""
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register API blueprint
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        """Serve the frontend's index.html."""
        return app.send_static_file("index.html")

    return app