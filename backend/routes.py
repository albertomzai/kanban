import json
import os
from flask import Blueprint, request, jsonify, abort

tasks_bp = Blueprint('tasks', __name__)

# Path to the tasks file (root of project)
TASKS_FILE = os.path.join(os.getcwd(), 'tasks.json')

def _read_tasks():
    """Read tasks from TASKS_FILE. Return a list of task dicts."""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file does not exist, start with empty list
        return []

def _write_tasks(tasks):
    """Write the given tasks list to TASKS_FILE."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)

def _generate_id(existing_tasks):
    """Return a new unique integer ID based on existing tasks."""
    if not existing_tasks:
        return 1
    max_id = max(task.get('id', 0) for task in existing_tasks)
    return max_id + 1

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks as JSON."""
    tasks = _read_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task. Expects JSON with 'content' and optional 'state'."""
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        abort(400, description='Content is required.')

    tasks = _read_tasks()
    new_task = {
        'id': _generate_id(tasks),
        'content': content,
        'state': data.get('state', 'Por Hacer')
    }
    tasks.append(new_task)
    _write_tasks(tasks)

    return jsonify(new_task), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update content or state of an existing task."""
    data = request.get_json() or {}
    tasks = _read_tasks()

    for task in tasks:
        if task.get('id') == task_id:
            # Update fields if provided
            if 'content' in data:
                task['content'] = data['content']
            if 'state' in data:
                task['state'] = data['state']
            _write_tasks(tasks)
            return jsonify(task), 200

    abort(404, description='Task not found.')

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID."""
    tasks = _read_tasks()
    new_tasks = [t for t in tasks if t.get('id') != task_id]

    if len(new_tasks) == len(tasks):
        abort(404, description='Task not found.')

    _write_tasks(new_tasks)
    return '', 204