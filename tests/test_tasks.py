import json

import pytest
from backend import tasks

@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    # Create a temporary tasks.json file
    tmp = tmp_path / "tasks.json"
    monkeypatch.setattr(tasks, "_TASKS_FILE", str(tmp))
    return tmp

def test_load_and_save(temp_file):
    # Ensure load returns empty list when file absent
    assert tasks.load_tasks() == []

    # Save a sample task list
    sample = [{"id": 1, "content": "Sample", "state": "Por Hacer"}]
    tasks.save_tasks(sample)

    # Load again and verify content
    loaded = tasks.load_tasks()
    assert loaded == sample

def test_get_next_id(temp_file):
    # Empty list returns 1
    assert tasks.get_next_id([]) == 1

    # Non-empty list increments correctly
    sample = [{"id": 5, "content": "A", "state": "Por Hacer"}]
    assert tasks.get_next_id(sample) == 6