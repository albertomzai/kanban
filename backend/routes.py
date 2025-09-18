# backend/routes.py

import json
import os
import threading
from typing import List, Dict, Any, Optional

from flask import request, jsonify, current_app, abort

from . import tasks_bp

# Path to the tasks.json file in project root
_TASKS_FILE = os.path.join(os.getcwd(), 'tasks.json')

# Simple lock for concurrent access
_lock = threading.Lock()

# Allowed statuses
_ALLOWED_STATUS = {'Por Hacer', 'En Progreso', 'Hecho'}

def _read_tasks() -> List[Dict[str, Any]]:
    """Read tasks from the JSON file. Returns an empty list if file not found."""
    with _lock:
        try:
            with open(_TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

def _write_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Write the list of tasks to the JSON file."""
    with _lock:
        with open(_TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

def _validate_task_payload(data: Dict[str, Any], for_update: bool = False) -> None:
    """Validate incoming task payloads. Raises abort(400) on failure."""
    if not isinstance(data, dict):
        abort(400, description='Payload must be a JSON object.')

    if 'content' in data:
        if not isinstance(data['content'], str) or not data['content'].strip():
            abort(400, description='Content must be a non-empty string.')

    if 'status' in data:
        if data['status'] not in _ALLOWED_STATUS:
            abort(400, description=f"Status must be one of {_ALLOWED_STATUS}.")

    # For creation we require content; for update it's optional
    if not for_update and 'content' not in data:
        abort(400, description='Content field is required.')

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks as JSON."""
    tasks = _read_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task with content and optional status."""
    data = request.get_json(force=True)
    _validate_task_payload(data, for_update=False)

    tasks = _read_tasks()
    next_id = max((t['id'] for t in tasks), default=0) + 1

    new_task: Dict[str, Any] = {
        'id': next_id,
        'content': data['content'].strip(),
        'status': data.get('status', 'Por Hacer')
    }

    tasks.append(new_task)
    _write_tasks(tasks)

    return jsonify(new_task), 201

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int):
    """Update the content or status of an existing task."""
    data = request.get_json(force=True)
    _validate_task_payload(data, for_update=True)

    tasks = _read_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404, description='Task not found.')

    if 'content' in data:
        task['content'] = data['content'].strip()
    if 'status' in data:
        task['status'] = data['status']

    _write_tasks(tasks)

    return jsonify(task), 200

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int):
    """Delete a task by its ID."""
    tasks = _read_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]

    if len(new_tasks) == len(tasks):
        abort(404, description='Task not found.')

    _write_tasks(new_tasks)

    return jsonify({'message': 'Task deleted.'}), 200