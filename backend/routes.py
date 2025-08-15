from flask import Blueprint, request, jsonify, abort
import json

from .tasks_storage import cargar_tareas, guardar_tareas

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks as JSON."""
    try:
        tareas = cargar_tareas()
    except Exception as e:
        abort(400, description=str(e))
    return jsonify(tareas)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task with content and default state 'Por Hacer'."""
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        abort(400, description='Content is required')

    tareas = cargar_tareas()
    new_id = max([t['id'] for t in tareas], default=0) + 1
    new_task = {'id': new_id, 'content': content, 'state': 'Por Hacer'}
    tareas.append(new_task)
    guardar_tareas(tareas)
    return jsonify(new_task), 201

@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """Update content or state of an existing task."""
    data = request.get_json() or {}
    tareas = cargar_tareas()

    task = next((t for t in tareas if t['id'] == id), None)
    if not task:
        abort(404, description='Task not found')

    content = data.get('content', task['content'])
    state = data.get('state', task['state'])

    task.update({'content': content, 'state': state})
    guardar_tareas(tareas)
    return jsonify(task)

@tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """Delete a task by id."""
    tareas = cargar_tareas()

    new_tasks = [t for t in tareas if t['id'] != id]
    if len(new_tasks) == len(tareas):
        abort(404, description='Task not found')

    guardar_tareas(new_tasks)
    return '', 204