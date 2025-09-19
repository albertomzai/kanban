"""Utility module for reading and writing tasks to a JSON file."""

import json
import os
from threading import Lock

_TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")
_lock = Lock()

def load_tasks():
    """Load tasks from the JSON file, returning a list."""
    with _lock:
        try:
            with open(_TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, start with empty list
            return []

def save_tasks(tasks):
    """Persist the given task list to the JSON file."""
    with _lock:
        with open(_TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

def get_next_id(tasks):
    """Return the next incremental ID based on existing tasks."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1