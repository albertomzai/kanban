from flask import Blueprint, jsonify, request, abort
import os
import json

api_bp = Blueprint('api', __name__)
TASKS_FILE = 'tasks.json'

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    if not os.path.exists(TASKS_FILE):
        return jsonify([]), 200
    with open(TASKS_FILE, 'r') as file:
        tasks = json.load(file)
    return jsonify(tasks), 200

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description='Invalid task data')
    with open(TASKS_FILE, 'r+') as file:
        tasks = json.load(file) if os.path.exists(TASKS_FILE) else []
        new_task = {'id': len(tasks) + 1, 'content': data['content'], 'state': 'Por Hacer'}
        tasks.append(new_task)
        file.seek(0)
        json.dump(tasks, file, indent=4)
    return jsonify(new_task), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data or ('content' not in data and 'state' not in data):
        abort(400, description='Invalid task data')
    with open(TASKS_FILE, 'r+') as file:
        tasks = json.load(file) if os.path.exists(TASKS_FILE) else []
        for task in tasks:
            if task['id'] == task_id:
                task.update(data)
                break
        else:
            abort(404, description='Task not found')
        file.seek(0)
        json.dump(tasks, file, indent=4)
    return jsonify(next(task for task in tasks if task['id'] == task_id)), 200

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with open(TASKS_FILE, 'r+') as file:
        tasks = json.load(file) if os.path.exists(TASKS_FILE) else []
        for task in tasks[:]:
            if task['id'] == task_id:
                tasks.remove(task)
                break
        else:
            abort(404, description='Task not found')
        file.seek(0)
        json.dump(tasks, file, indent=4)
    return '', 204