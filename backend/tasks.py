import json
from pathlib import Path

# Path to the JSON file relative to this module
_TASKS_FILE = Path(__file__).parent / 'tasks.json'

def load_tasks():
    """Load tasks from the JSON file. Returns a list of task dicts."""
    if not _TASKS_FILE.exists():
        return []
    with open(_TASKS_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    """Persist the list of tasks to the JSON file."""
    with open(_TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)

def get_next_id(tasks):
    """Return an incremented ID based on existing tasks."""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

ALLOWED_STATUSES = {'Por Hacer', 'En Progreso', 'Hecho'}

def validate_task_data(data, require_status=True):
    """Validate incoming task data.

    Returns a tuple (content, status). Raises ValueError on failure."""
    if not isinstance(data, dict):
        raise ValueError('Data must be JSON object')

    content = data.get('content')
    status = data.get('status', 'Por Hacer' if require_status else None)

    if content is None or not isinstance(content, str) or not content.strip():
        raise ValueError('Content must be a non-empty string')

    if status is not None:
        if status not in ALLOWED_STATUSES:
            raise ValueError(f'Status must be one of {sorted(ALLOWED_STATUSES)}')

    return content.strip(), status