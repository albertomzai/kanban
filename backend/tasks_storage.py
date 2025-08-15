import json
from pathlib import Path

TASKS_FILE = Path(__file__).parent / 'tasks.json'

def cargar_tareas():
    """Load tasks from the JSON file. Returns a list of task dicts."""
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, start fresh
        return []

def guardar_tareas(tareas):
    """Persist the given list of tasks to the JSON file."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)