import json
from pathlib import Path
from typing import List, Dict, Any

from flask import Blueprint, request, jsonify, abort

# Define the path to the tasks.json file relative to this module.
TASKS_FILE: Path = Path(__file__).resolve().parent.parent / 'tasks.json'

tasks_bp = Blueprint('tasks', __name__)

def _load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from the JSON file.

    Returns an empty list if the file does not exist or is empty."""
    try:
        with TASKS_FILE.open('r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Corrupted file – reset to empty.
        return []

def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Persist the given list of tasks to the JSON file."""
    with TASKS_FILE.open('w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks as JSON."""
    tasks = _load_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task.

    Expects JSON body with 'content' and optionally 'state'.
    Assigns a unique integer ID."""
    data = request.get_json() or {}
    content = data.get('content')
    state = data.get('state', 'Por Hacer')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    tasks = _load_tasks()
    new_id = max((task['id'] for task in tasks), default=0) + 1
    new_task = {'id': new_id, 'content': content, 'state': state}
    tasks.append(new_task)
    _save_tasks(tasks)

    return jsonify(new_task), 201

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task's content or state."""
    data = request.get_json() or {}

    tasks = _load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            # Update fields if provided.
            if 'content' in data:
                task['content'] = data['content']
            if 'state' in data:
                task['state'] = data['state']
            _save_tasks(tasks)
            return jsonify(task), 200

    abort(404, description='Task not found')

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by its ID."""
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]

    if len(new_tasks) == len(tasks):
        abort(404, description='Task not found')

    _save_tasks(new_tasks)
    return jsonify({}), 200