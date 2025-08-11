# tasks.py - helper for task persistence
import json
import os
from pathlib import Path

# Default path to the JSON file
TASKS_FILE = Path(__file__).parent / 'tasks.json'


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)