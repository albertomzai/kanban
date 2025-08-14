import json
from flask import Blueprint, request, jsonify, current_app
from .tasks import load_tasks, save_tasks, get_next_id, validate_task_data

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Return all tasks as JSON."""
    tasks = load_tasks()
    return jsonify(tasks), 200

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task. Expects JSON with 'content' and optional 'status'."""
    data = request.get_json() or {}
    try:
        content, status = validate_task_data(data, require_status=False)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    tasks = load_tasks()
    task_id = get_next_id(tasks)
    new_task = {'id': task_id, 'content': content, 'status': status}
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task's content or status."""
    data = request.get_json() or {}
    try:
        content, status = validate_task_data(data, require_status=False)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if content is not None:
                task['content'] = content
            if status is not None:
                task['status'] = status
            save_tasks(tasks)
            return jsonify(task), 200

    return jsonify({'error': 'Task not found'}), 404

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404

    save_tasks(new_tasks)
    return jsonify({'message': 'Deleted'}), 200