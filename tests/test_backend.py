import json
import os
import tempfile
from pathlib import Path
import pytest

# Import the Flask app and TASKS_FILE from the backend package
from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    # Create a temporary tasks.json file for the duration of the test
    temp_file = tmp_path / "tasks.json"
    # Ensure the file exists and is empty
    temp_file.write_text("[]")
    # Patch TASKS_FILE to point to our temp file
    monkeypatch.setattr("backend.app.TASKS_FILE", str(temp_file))
    return temp_file

def test_delete_task_success(client, temp_tasks_file):
    # Arrange: create a task via POST so it exists in the temp file
    response = client.post(
        "/api/tasks",
        json={"content": "Test task", "state": "Por Hacer"},
    )
    assert response.status_code == 201
    created_task = response.get_json()
    task_id = created_task["id"]

    # Act: delete the task
    del_resp = client.delete(f"/api/tasks/{task_id}")

    # Assert
    assert del_resp.status_code == 204
    # Verify that the task is no longer in the file
    tasks_data = json.loads(temp_tasks_file.read_text())
    assert not any(t["id"] == task_id for t in tasks_data)

def test_delete_task_not_found(client, temp_tasks_file):
    # Act: attempt to delete a non‑existent task
    resp = client.delete("/api/tasks/9999")
    # Assert
    assert resp.status_code == 404
