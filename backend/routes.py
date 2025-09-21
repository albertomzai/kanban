from flask import jsonify, request, Blueprint, abort

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = repository.load_tasks()
    return jsonify([task.__dict__ for task in tasks])

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True)
    if not data or 'content' not in data:
        abort(400, 'Content is required')

    task_id = str(hash(data['content']))
    new_task = Task(task_id, data['content'], 'To Do')
    repository.save_tasks([new_task])
    return jsonify({'id': new_task.id}), 201

@api_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id: str):
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'No data provided')

    try:
        task = repository.load_tasks()[int(task_id)]
        task.content = data['content'] if 'content' in data else task.content
        task.state = data['state'] if 'state' in data else task.state
        repository.save_tasks([task])
        return jsonify({'id': task_id}), 200
    except IndexError:
        abort(404, f'Task {task_id} not found')

@api_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id: str):
    try:
        tasks = repository.load_tasks()
        tasks.pop(int(task_id))
        repository.save_tasks(tasks)
        return jsonify({'status': 'success'}), 204
    except IndexError:
        abort(404, f'Task {task_id} not found')
