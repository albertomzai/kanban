# backend/routes.py
import json
from flask import Blueprint, request, jsonify, current_app
import os

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')
DATA_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

# Helper to load and save tasks

def _load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    tasks = _load_tasks()
    return jsonify(tasks), 200

@tasks_bp.route('', methods=['POST'])
def create_task():
    data = request.get_json(force=True)
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'Content required'}), 400
    tasks = _load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {'id': new_id, 'content': content, 'state': 'Por Hacer'}
    tasks.append(task)
    _save_tasks(tasks)
    return jsonify(task), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json(force=True)
    tasks = _load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    content = data.get('content')
    state = data.get('state')
    if content is not None:
        task['content'] = content.strip()
    if state in ['Por Hacer', 'En Progreso', 'Hecho']:
        task['state'] = state
    _save_tasks(tasks)
    return jsonify(task), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    _save_tasks(new_tasks)
    return '', 204
