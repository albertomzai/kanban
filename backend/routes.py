import json
import os
from typing import List, Dict, Any, Optional

from flask import Blueprint, request, jsonify, abort


# Ruta absoluta del archivo de tareas
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')


api_bp = Blueprint('api', __name__)


def _load_tasks() -> List[Dict[str, Any]]:
    """Carga las tareas desde TASKS_FILE."""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Guarda la lista de tareas en TASKS_FILE."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Devuelve todas las tareas."""
    tasks = _load_tasks()
    return jsonify(tasks), 200


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Crea una nueva tarea con estado 'Por Hacer'."""
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    content = data.get('content')
    if not content or not isinstance(content, str):
        abort(400, description='Missing or invalid "content" field')

    tasks = _load_tasks()
    new_id = max([t['id'] for t in tasks], default=0) + 1
    new_task = {
        'id': new_id,
        'content': content,
        'status': 'Por Hacer'
    }
    tasks.append(new_task)
    _save_tasks(tasks)

    return jsonify(new_task), 201


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Actualiza el contenido o estado de una tarea existente."""
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    content: Optional[str] = data.get('content')
    status: Optional[str] = data.get('status')

    tasks = _load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        abort(404, description='Task not found')

    if content is not None:
        if not isinstance(content, str):
            abort(400, description='Invalid "content" field')
        task['content'] = content

    if status is not None:
        if status not in ['Por Hacer', 'En Progreso', 'Hecho']:
            abort(400, description='Invalid status value')
        task['status'] = status

    _save_tasks(tasks)
    return jsonify(task), 200


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Elimina una tarea existente."""
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        abort(404, description='Task not found')

    _save_tasks(new_tasks)
    return '', 204