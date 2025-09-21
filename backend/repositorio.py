from pathlib import Path
import json

from .modelos import Task

TASKS_FILE = Path('tasks.json')

def load_tasks() -> list[Task]:
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks: list[Task]):
    with open(TASKS_FILE, 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)