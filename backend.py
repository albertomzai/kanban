from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

TASKS_FILE = 'tasks.json'
# Ensure tasks file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

# Helper functions to read/write tasks

def load_tasks():
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)

# Serve frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# API endpoints
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json(force=True)
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {'id': new_id, 'content': content, 'status': 'Por Hacer'}
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json(force=True)
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task.update({k: v for k, v in data.items() if k in ['content', 'status']})
            save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'error': f'Task {task_id} not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    filtered = [t for t in tasks if t['id'] != task_id]
    if len(filtered) == len(tasks):
        return jsonify({'error': f'Task {task_id} not found'}), 404
    save_tasks(filtered)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)