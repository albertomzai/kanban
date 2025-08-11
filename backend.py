"""
Flask backend for Kanban tasks.
Provides CRUD API endpoints and serves the frontend index.html from the static folder.
All task data is persisted in a JSON file (tasks.json).
"""

import json
import os
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Path to the JSON file that stores tasks
TASKS_FILE = os.path.join(os.getcwd(), 'tasks.json')

# ---------------------------------------------------------------------------
# Helper functions for task persistence
# ---------------------------------------------------------------------------

def load_tasks():
    """Load tasks from TASKS_FILE. Return an empty list if file does not exist.
    Each task is a dict with at least keys: id, content, status.
    """
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Corrupted file – start fresh
        return []


def save_tasks(tasks):
    """Persist the list of tasks to TASKS_FILE."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    """Serve the frontend application."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    # Generate a new unique ID
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {
        'id': new_id,
        'content': content,
        'status': data.get('status', 'Por Hacer')
    }
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            # Update allowed fields
            if 'content' in data:
                task['content'] = data['content']
            if 'status' in data:
                task['status'] = data['status']
            save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Delete the task with the given ID.
    Returns HTTP 204 on success or 404 if the task does not exist.
    """
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            # Remove and persist
            del tasks[i]
            save_tasks(tasks)
            return '', 204
    return jsonify({'error': 'Task not found'}), 404

# ---------------------------------------------------------------------------
# Run the application (debug mode for development)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
