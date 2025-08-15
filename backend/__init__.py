import os

from flask import Flask, jsonify, request, Blueprint
import json

# Path to the tasks JSON file
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')

# Create a blueprint for task routes
tasks_bp = Blueprint('tasks', __name__)

def _load_tasks():
    """Load tasks from the JSON file.

    Returns:
        list: List of task dictionaries.
    """
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file does not exist, start with an empty list
        return []

def _save_tasks(tasks):
    """Persist tasks to the JSON file.

    Args:
        tasks (list): List of task dictionaries to save.
    """
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks.

    Returns:
        Response: JSON list of tasks.
    """
    return jsonify(_load_tasks()), 200

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task.

    Expects JSON with 'content' and optional 'state'.
    """
    data = request.get_json() or {}
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    tasks = _load_tasks()
    new_id = max((t['id'] for t in tasks), default=0) + 1
    new_task = {
        'id': new_id,
        'content': content,
        'state': data.get('state', 'Por Hacer')
    }

    tasks.append(new_task)
    _save_tasks(tasks)

    return jsonify(new_task), 201

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task.

    Expects JSON with optional 'content' and/or 'state'.
    """
    data = request.get_json() or {}

    tasks = _load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if 'content' in data:
                content = data['content'].strip()
                if not content:
                    return jsonify({'error': 'Content cannot be empty'}), 400
                task['content'] = content
            if 'state' in data:
                task['state'] = data['state']
            _save_tasks(tasks)
            return jsonify(task), 200

    return jsonify({'error': 'Task not found'}), 404

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID."""
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]

    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404

    _save_tasks(new_tasks)
    return jsonify({}), 200

def create_app():
    """Factory function to create and configure the Flask app."""
    # The static folder is one level up in 'frontend'
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the blueprint
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def index():
        """Serve the frontend index.html."""
        return app.send_static_file('index.html')

    return app

# Create a global app instance for convenience
app = create_app()