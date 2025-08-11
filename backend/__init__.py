from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Archivo donde se persisten las tareas
TASKS_FILE = 'tasks.json'

# Ruta para servir el frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Helper: cargar tareas desde archivo
def _load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Helper: guardar tareas a archivo
def _save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# GET /api/tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = _load_tasks()
    return jsonify(tasks), 200

# POST /api/tasks
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    content = data.get('content', '')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    tasks = _load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {'id': new_id, 'content': content, 'state': 'Por Hacer'}
    tasks.append(task)
    _save_tasks(tasks)
    return jsonify(task), 201

# PUT /api/tasks/<int:id>
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json() or {}
    tasks = _load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['content'] = data.get('content', task['content'])
            task['state'] = data.get('state', task['state'])
            _save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

# DELETE /api/tasks/<int:id>
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    _save_tasks(new_tasks)
    return '', 204

# Si se ejecuta directamente, lanzar el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)