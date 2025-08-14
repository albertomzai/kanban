import json
from flask import Blueprint, request, jsonify, current_app, abort

tasks_bp = Blueprint('tasks', __name__)

ALLOWED_STATUSES = ['Por Hacer', 'En Progreso', 'Hecho']

def _get_next_id(tasks):
    return max((task.get('id', 0) for task in tasks), default=0) + 1

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = current_app.config['TASKS']
    return jsonify(tasks)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        abort(400, description='Content is required')

    status = data.get('status', 'Por Hacer')
    if status not in ALLOWED_STATUSES:
        abort(400, description=f'Status must be one of {ALLOWED_STATUSES}')

    tasks = current_app.config['TASKS']
    new_task = {
        'id': _get_next_id(tasks),
        'content': content,
        'status': status
    }
    tasks.append(new_task)
    try:
        _save_tasks(current_app.config['TASKS_FILE'], tasks)
    except Exception as e:
        abort(500, description=str(e))

    return jsonify(new_task), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = current_app.config['TASKS']
    task = next((t for t in tasks if t.get('id') == task_id), None)
    if not task:
        abort(404, description='Task not found')

    content = data.get('content', task['content'])
    status = data.get('status', task['status'])

    if status not in ALLOWED_STATUSES:
        abort(400, description=f'Status must be one of {ALLOWED_STATUSES}')

    task['content'] = content
    task['status'] = status

    try:
        _save_tasks(current_app.config['TASKS_FILE'], tasks)
    except Exception as e:
        abort(500, description=str(e))

    return jsonify(task)

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = current_app.config['TASKS']
    task_index = next((i for i, t in enumerate(tasks) if t.get('id') == task_id), None)
    if task_index is None:
        abort(404, description='Task not found')

    deleted_task = tasks.pop(task_index)
    try:
        _save_tasks(current_app.config['TASKS_FILE'], tasks)
    except Exception as e:
        abort(500, description=str(e))

    return jsonify(deleted_task), 200