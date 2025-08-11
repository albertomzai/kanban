"""
Unit tests for the backend API.
Uses Flask test client and monkeypatch to isolate file operations.
"""

import json
import os
from pathlib import Path
import pytest

# Import the Flask app
from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    """Provide a temporary tasks.json file for each test."""
    temp_file = tmp_path / "tasks.json"
    # Ensure the file exists with an empty list
    temp_file.write_text("[]", encoding="utf-8")
    # Patch the TASKS_FILE path in the backend module
    monkeypatch.setattr("backend.TASKS_FILE", str(temp_file))
    return temp_file

def test_delete_existing_task(client, temp_tasks_file):
    # Create a task directly in the file
    tasks = [{"id": 1, "content": "Test Task", "status": "Por Hacer"}]
    temp_tasks_file.write_text(json.dumps(tasks), encoding="utf-8")

    response = client.delete("/api/tasks/1")
    assert response.status_code == 204
    # Verify the file is now empty
    remaining = json.loads(temp_tasks_file.read_text(encoding="utf-8"))
    assert remaining == []

def test_delete_nonexistent_task(client, temp_tasks_file):
    # Ensure file has no tasks
    temp_tasks_file.write_text("[]", encoding="utf-8")

    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
    assert b"Task not found" in response.data
