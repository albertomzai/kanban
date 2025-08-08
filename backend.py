# -*- coding: utf-8 -*-
"""
Flask application exposing a REST API for a Kanban board.

The app serves the SPA from the ``static`` folder and exposes the following
endpoints:

  * GET    /api/tasks          – list all tasks
  * POST   /api/tasks          – create a new task
  * PUT    /api/tasks/<int:id> – update an existing task
  * DELETE /api/tasks/<int:id> – delete a task

All data is persisted in ``tasks.json`` by the :mod:`tasks_manager` module.
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, "static")
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")
ALLOWED_STATES = {"Por Hacer", "En Progreso", "Hecho"}

# ---------------------------------------------------------------------------
# Flask app setup
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=STATIC_FOLDER)
CORS(app)  # Allow cross‑origin requests from the same domain

# Import after CORS to avoid circular imports
from tasks_manager import (
    load_tasks,
    save_tasks,
    generate_task_id,
    find_task_by_id,
    delete_task_by_id,
)

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def _validate_state(state: str) -> None:
    """Raise a ValueError if *state* is not allowed.

    Args:
        state: The state string to validate.

    Raises:
        ValueError: If the state is invalid.
    """
    if state not in ALLOWED_STATES:
        raise ValueError(
            f"Invalid state '{state}'. Allowed values are {sorted(ALLOWED_STATES)}"
        )

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Serve the SPA entry point.

    The front‑end is a single ``index.html`` file located in the static folder.
    """
    return send_from_directory(app.static_folder, "index.html")

# API routes ---------------------------------------------------------------
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as JSON.

    Response format:
        {
            "tasks": [
                {"id": int, "content": str, "state": str},
                ...
            ]
        }
    """
    tasks = load_tasks(TASKS_FILE)
    return jsonify({"tasks": tasks}), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task.

    Expected JSON body:
        {"content": str, "state": "Por Hacer"}

    The ``state`` field is validated against :data:`ALLOWED_STATES`.
    A unique integer ID is generated automatically.
    """
    data = request.get_json(force=True)
    content = data.get("content")
    state = data.get("state", "Por Hacer")

    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "'content' must be a non‑empty string."}), 400

    try:
        _validate_state(state)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    tasks = load_tasks(TASKS_FILE)
    new_id = generate_task_id(tasks)
    new_task = {"id": new_id, "content": content.strip(), "state": state}
    tasks.append(new_task)
    save_tasks(TASKS_FILE, tasks)
    return jsonify(new_task), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task.

    The request body may contain one or both of:
        {"content": str, "state": str}
    """
    data = request.get_json(force=True)
    content = data.get("content")
    state = data.get("state")

    if content is not None and (not isinstance(content, str) or not content.strip()):
        return jsonify({"error": "'content' must be a non‑empty string."}), 400

    if state is not None:
        try:
            _validate_state(state)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    tasks = load_tasks(TASKS_FILE)
    task = find_task_by_id(tasks, task_id)
    if not task:
        return jsonify({"error": f"Task with id {task_id} not found."}), 404

    if content is not None:
        task["content"] = content.strip()
    if state is not None:
        task["state"] = state

    save_tasks(TASKS_FILE, tasks)
    return jsonify(task), 200

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID.

    Response on success:
        {"message": "Task deleted successfully."}
    """
    tasks = load_tasks(TASKS_FILE)
    if not delete_task_by_id(tasks, task_id):
        return jsonify({"error": f"Task with id {task_id} not found."}), 404
    save_tasks(TASKS_FILE, tasks)
    return jsonify({"message": "Task deleted successfully."}), 200

# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error."}), 500

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Ensure tasks.json exists before starting the server
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            f.write("[]")
    app.run(host="0.0.0.0", port=5000, debug=True)
