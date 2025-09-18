import json
import os

from flask import Blueprint, request, jsonify, abort

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Path to the tasks JSON file located in the backend package directory.
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

def _load_tasks():
    """Load tasks from TASKS_FILE. Return an empty list if file not found."""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def _save_tasks(tasks):
    """Persist the given list of tasks to TASKS_FILE."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all existing tasks."""
    return jsonify(_load_tasks()), 200

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task with the provided content. State defaults to 'Por Hacer'."""
    data = request.get_json() or {}
    content = data.get('content')

    if not content:
        abort(400, description='Content is required.')

    tasks = _load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {"id": new_id, "content": content, "state": "Por Hacer"}
    tasks.append(task)
    _save_tasks(tasks)

    return jsonify(task), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update the content and/or state of an existing task."""
    data = request.get_json() or {}
    tasks = _load_tasks()

    for task in tasks:
        if task['id'] == task_id:
            if 'content' in data:
                task['content'] = data['content']
            if 'state' in data:
                task['state'] = data['state']
            _save_tasks(tasks)
            return jsonify(task), 200

    abort(404, description='Task not found.')

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete the task identified by task_id."""
    tasks = _load_tasks()

    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        abort(404, description='Task not found.')

    _save_tasks(new_tasks)
    return '', 204