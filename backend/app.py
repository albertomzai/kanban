import os
import json
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Path to the tasks persistence file
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

# Ensure the tasks file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_tasks():
    """Load all tasks from the JSON file."""
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    """Persist the given list of tasks to the JSON file."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)

# ---------- API Endpoints ----------
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200

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

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['content'] = data.get('content', task['content'])
            task['status'] = data.get('status', task['status'])
            save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    save_tasks(new_tasks)
    return jsonify({'message': 'Task deleted'}), 200

# ---------- Frontend Serving ----------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
