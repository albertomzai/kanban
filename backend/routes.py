"""Blueprint that implements the Kanban API endpoints."""

import json
import os
from typing import List, Dict, Any

from flask import Blueprint, request, jsonify, abort

# Path to the JSON file that stores tasks
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

# Valid states for a task
VALID_STATES = {'Por Hacer', 'En Progreso', 'Hecho'}

tasks_bp = Blueprint('tasks_bp', __name__)

def _load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from the JSON file.

    Returns an empty list if the file does not exist or is malformed."""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, ValueError):
        # If the file is corrupted, start fresh
        return []

def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Persist tasks to the JSON file."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def _validate_task_payload(data: Dict[str, Any]) -> None:
    """Validate the payload for creating or updating a task.

    Raises an HTTP 400 error if validation fails."""
    if not isinstance(data, dict):
        abort(400, description='Payload must be a JSON object')

    content = data.get('content')
    state = data.get('state', 'Por Hacer')  # default to 'Por Hacer' on create

    if not isinstance(content, str) or not content.strip():
        abort(400, description='"content" must be a non‑empty string')

    if state not in VALID_STATES:
        abort(400, description=f'State must be one of {sorted(VALID_STATES)}')

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks as a JSON list."""
    tasks = _load_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task.

    Expects JSON payload with 'content'.
    The new task receives an auto‑incremented integer id and the default state."""
    data = request.get_json() or {}
    _validate_task_payload(data)

    tasks = _load_tasks()
    # Generate next ID
    next_id = max((t['id'] for t in tasks), default=0) + 1

    new_task = {
        'id': next_id,
        'content': data['content'].strip(),
        'state': data.get('state', 'Por Hacer')
    }
    tasks.append(new_task)
    _save_tasks(tasks)

    return jsonify(new_task), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task.

    Payload may contain 'content' and/or 'state'."""
    data = request.get_json() or {}

    # Validate only the fields that are present
    if 'content' in data:
        if not isinstance(data['content'], str) or not data['content'].strip():
            abort(400, description='"content" must be a non‑empty string')

    if 'state' in data:
        if data['state'] not in VALID_STATES:
            abort(400, description=f'State must be one of {sorted(VALID_STATES)}')

    tasks = _load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            # Apply updates
            if 'content' in data:
                task['content'] = data['content'].strip()
            if 'state' in data:
                task['state'] = data['state']
            _save_tasks(tasks)
            return jsonify(task), 200

    abort(404, description='Task not found')

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by its ID."""
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]

    if len(new_tasks) == len(tasks):
        abort(404, description='Task not found')

    _save_tasks(new_tasks)
    return '', 204