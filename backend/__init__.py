import json
import os
from threading import Lock

from flask import Flask, jsonify, request, abort, current_app

# Global lock for thread‑safe file access
_file_lock = Lock()

def _load_tasks(filepath):
    """Load tasks from a JSON file.

    Returns a list of task dicts. If the file does not exist or is empty,
    an empty list is returned.
    """
    if not os.path.exists(filepath):
        return []

    with _file_lock:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            # Log the error in a real application
        return []

def _save_tasks(filepath, tasks):
    """Persist tasks to a JSON file atomically."""
    with _file_lock:
        temp_path = f"{filepath}.tmp"
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2)
            os.replace(temp_path, filepath)
        except Exception as e:
            # In a real app we would log this error
            raise RuntimeError("Failed to write tasks file") from e

def create_app():
    """Application factory for the Kanban backend."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Load tasks at startup and store in config
    task_file = os.path.join(os.path.dirname(__file__), 'tasks.json')
    current_app.config['TASKS_FILE'] = task_file
    current_app.config['TASKS'] = _load_tasks(task_file)

    # Register the tasks blueprint
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return current_app.send_static_file('index.html')

    return app