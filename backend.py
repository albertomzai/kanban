from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Path to the tasks file
TASKS_FILE = os.path.join(os.getcwd(), 'tasks.json')

# Helper functions for data persistence

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)

# Serve the frontend
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
    task = {
        'id': new_id,
        'content': content,
        'state': data.get('state', 'Por Hacer')
    }
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json(force=True)
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['content'] = data.get('content', task['content'])
            task['state'] = data.get('state', task['state'])
            save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted = tasks.pop(i)
            save_tasks(tasks)
            return jsonify({'message': f"Task {task_id} deleted successfully."}), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
