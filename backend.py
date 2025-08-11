from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Ruta para servir el frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Archivo donde se guardan las tareas
TASKS_FILE = os.path.join(os.getcwd(), 'tasks.json')

# Funciones auxiliares para leer y escribir tareas

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
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# GET /api/tasks: Devuelve todas las tareas existentes.
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = load_tasks()
        return jsonify(tasks), 200
    except Exception as e:
        app.logger.exception('Error al cargar tareas')
        return '', 500

# POST /api/tasks: Crea una nueva tarea.
@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'Content required'}), 400
        tasks = load_tasks()
        new_id = max([t['id'] for t in tasks], default=0) + 1
        new_task = {
            'id': new_id,
            'content': data['content'],
            'status': data.get('status', 'Por Hacer')
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return jsonify(new_task), 201
    except Exception as e:
        app.logger.exception('Error al crear tarea')
        return '', 500

# PUT /api/tasks/<id>: Actualiza una tarea existente.
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        tasks = load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task.update({k: v for k, v in data.items() if k in ['content', 'status']})
                save_tasks(tasks)
                return jsonify(task), 200
        return '', 404
    except Exception as e:
        app.logger.exception('Error al actualizar tarea')
        return '', 500

# DELETE /api/tasks/<id>: Elimina una tarea.
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        tasks = load_tasks()
        new_tasks = [t for t in tasks if t['id'] != task_id]
        if len(new_tasks) == len(tasks):
            # No se encontró la tarea
            return '', 404
        save_tasks(new_tasks)
        return '', 204
    except Exception as e:
        app.logger.exception('Error al eliminar tarea')
        return '', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
