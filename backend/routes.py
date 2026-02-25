from flask import Blueprint, request, jsonify
from .storage import cargar_tareas, guardar_tareas

# Creación del Blueprint para la API
api_bp = Blueprint('api', __name__)


@api_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Endpoint para obtener todas las tareas.
    Devuelve una lista JSON con todas las tareas almacenadas.
    """
    tareas = cargar_tareas()
    return jsonify(tareas)


@api_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Endpoint para crear una nueva tarea.
    Espera un JSON con el campo 'content'.
    Asigna un ID único y el estado inicial 'Por Hacer'.
    """
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'El contenido es obligatorio'}), 400

    tareas = cargar_tareas()
    # Generación de ID simple (máximo existente + 1)
    new_id = max([t.get('id', 0) for t in tareas], default=0) + 1
    
    nueva_tarea = {
        'id': new_id,
        'content': data['content'],
        'state': 'Por Hacer'
    }
    
    tareas.append(nueva_tarea)
    guardar_tareas(tareas)
    return jsonify(nueva_tarea), 201


@api_bp.route('/api/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    Endpoint para actualizar una tarea existente.
    Permite modificar el 'content' y/o el 'state' de la tarea.
    """
    tareas = cargar_tareas()
    tarea = next((t for t in tareas if t['id'] == id), None)
    
    if not tarea:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    data = request.get_json()
    if data:
        if 'content' in data:
            tarea['content'] = data['content']
        if 'state' in data:
            tarea['state'] = data['state']
    
    guardar_tareas(tareas)
    return jsonify(tarea)


@api_bp.route('/api/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """
    Endpoint para eliminar una tarea por su ID.
    """
    tareas = cargar_tareas()
    tareas_filtradas = [t for t in tareas if t['id'] != id]
    
    if len(tareas) == len(tareas_filtradas):
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    guardar_tareas(tareas_filtradas)
    return jsonify({'message': 'Tarea eliminada correctamente'})