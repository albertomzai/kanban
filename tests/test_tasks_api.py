import json
import os
import pytest
from backend import app as flask_app

# Use the same TASKS_FILE constant from the app for monkeypatching
TASKS_FILE = "tasks.json"

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    file = tmp_path / "test_tasks.json"
    # Redirect the TASKS_FILE variable in the app module
    monkeypatch.setattr("backend.app.TASKS_FILE", str(file))
    return file

# Helper to create a task via POST

def create_task(client, content, state="Por Hacer"):
    response = client.post(
        "/api/tasks",
        json={"content": content, "state": state},
    )
    assert response.status_code == 201
    return response.get_json()

def test_delete_task_success(client, temp_file):
    # Create a task first
    task = create_task(client, "Test Task")
    task_id = task["id"]
    # Ensure it exists
    resp_get = client.get("/api/tasks")
    assert any(t["id"] == task_id for t in resp_get.get_json())
    # Delete the task
    resp_del = client.delete(f"/api/tasks/{task_id}")
    assert resp_del.status_code == 200
    data = resp_del.get_json()
    assert data["message"] == "Task deleted"
    # Verify it's removed
    resp_get_after = client.get("/api/tasks")
    assert not any(t["id"] == task_id for t in resp_get_after.get_json())

def test_delete_nonexistent_task(client, temp_file):
    resp_del = client.delete("/api/tasks/9999")
    assert resp_del.status_code == 404
    data = resp_del.get_json()
    assert data["error"] == "Task not found"
