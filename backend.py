from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Path to the tasks file (will be monkeypatched in tests if needed)
TASKS_FILE = os.path.join(os.getcwd(), 'tasks.json')

# Helper functions for task persistence

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # If file is corrupted or unreadable, start fresh
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Serve the frontend index.html
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# GET all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200

# POST create a new task (content and default status 'Por Hacer')
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {
        'id': new_id,
        'content': content,
        'status': data.get('status', 'Por Hacer')
    }
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

# PUT update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t.update({k: v for k, v in data.items() if k in ['content', 'status']})
            save_tasks(tasks)
            return jsonify(t), 200
    return jsonify({'error': 'Task not found'}), 404

# DELETE a task by id
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t['id'] == task_id:
            del tasks[i]
            save_tasks(tasks)
            return '', 204
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)