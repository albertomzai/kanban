import json
import os
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS

# ---------------------------------------------------------------------------
# Configuration and globals
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder="static")
CORS(app)

# Path to the JSON file that stores tasks. It lives in the project root.
TASKS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tasks.json"))

# ---------------------------------------------------------------------------
# Utility functions for task persistence
# ---------------------------------------------------------------------------
def _load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Corrupted file – start fresh
            return []

def _save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

# ---------------------------------------------------------------------------
# Helper to find a task by ID
# ---------------------------------------------------------------------------
def _find_task(task_id, tasks):
    for t in tasks:
        if t.get("id") == task_id:
            return t
    return None

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    """Serve the single‑page application front‑end."""
    return send_from_directory(app.static_folder, 'index.html')

# API: GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = _load_tasks()
    return jsonify(tasks)

# API: POST create new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    if not content:
        abort(400, description='Content is required')
    tasks = _load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {
        'id': new_id,
        'content': content,
        'state': data.get('state', 'Por Hacer')
    }
    tasks.append(task)
    _save_tasks(tasks)
    return jsonify(task), 201

# API: PUT update task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = _load_tasks()
    task = _find_task(task_id, tasks)
    if not task:
        abort(404, description='Task not found')
    # Update fields if provided
    content = data.get('content')
    state = data.get('state')
    if content is not None:
        task['content'] = content.strip()
    if state is not None:
        task['state'] = state
    _save_tasks(tasks)
    return jsonify(task)

# API: DELETE task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = _load_tasks()
    task = _find_task(task_id, tasks)
    if not task:
        abort(404, description='Task not found')
    tasks.remove(task)
    _save_tasks(tasks)
    return '', 204
