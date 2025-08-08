# -*- coding: utf-8 -*-
"""
Utility module for loading, saving and manipulating task data.

All tasks are stored as a list of dictionaries in ``tasks.json``.
The functions here are intentionally small and pure to make them easy to test.
"""

import json
from typing import List, Dict, Optional

# Type alias for clarity
Task = Dict[str, object]


def load_tasks(filepath: str) -> List[Task]:
    """Load tasks from *filepath*.

    If the file does not exist or is empty, an empty list is returned.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(filepath: str, tasks: List[Task]) -> None:
    """Persist *tasks* to *filepath* in pretty JSON format."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def generate_task_id(tasks: List[Task]) -> int:
    """Return a new unique integer ID.

    IDs are monotonically increasing starting from 1.
    """
    if not tasks:
        return 1
    existing_ids = [task.get("id", 0) for task in tasks]
    return max(existing_ids) + 1


def find_task_by_id(tasks: List[Task], task_id: int) -> Optional[Task]:
    """Return the task with *task_id* or ``None`` if not found."""
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def delete_task_by_id(tasks: List[Task], task_id: int) -> bool:
    """Remove the task with *task_id* from *tasks*.

    Returns ``True`` if a task was removed, otherwise ``False``.
    """
    for i, task in enumerate(tasks):
        if task.get("id") == task_id:
            del tasks[i]
            return True
    return False
