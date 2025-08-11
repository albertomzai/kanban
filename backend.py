from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import logging

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuración del logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

# Helper para cargar y guardar tareas

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error al cargar tareas: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        logger.error(f"Error al guardar tareas: {e}")

# Ruta para servir el frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Endpoints de la API
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Content required'}), 400
    tasks = load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    task = {
        'id': new_id,
        'content': data['content'],
        'status': 'Por Hacer'
    }
    tasks.append(task)
    save_tasks(tasks)
    logger.info(f"Task created: {task}")
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task.update({k: v for k, v in data.items() if k in ['content', 'status']})
            save_tasks(tasks)
            logger.info(f"Task updated: {task}")
            return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        tasks = load_tasks()
        new_tasks = [t for t in tasks if t['id'] != task_id]
        if len(new_tasks) == len(tasks):
            return jsonify({'error': 'Task not found'}), 404
        save_tasks(new_tasks)
        logger.info(f"Task deleted: id={task_id}")
        return jsonify({'message': f'Task {task_id} deleted successfully.'}), 200
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)