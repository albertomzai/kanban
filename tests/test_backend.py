import json
from pathlib import Path

import pytest

# Import the Flask app from backend module
from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    """Provide a test client for the Flask application."""
    with flask_app.test_client() as c:
        yield c

@pytest.fixture(autouse=True)
def clean_tasks_file(tmp_path):
    """Ensure tests start with an empty tasks.json file.
    The fixture replaces TASKS_FILE with a temporary file during the test session.
    """
    original = str(TASKS_FILE)
    tmp = tmp_path / "tasks.json"
    # Monkeypatch the global variable in backend module
    import backend
    backend.TASKS_FILE = tmp
    yield
    # Restore original path after tests
    backend.TASKS_FILE = Path(original)

# Helper to read current tasks from file

def _read_tasks():
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def test_get_empty(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) and len(data) == 0

def test_create_task(client):
    payload = {"content": "Test task", "state": "Por Hacer"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    created = response.get_json()
    assert created["id"] == 1
    assert created["content"] == payload["content"]
    assert created["state"] == payload["state"]

    # Verify persistence
    tasks = _read_tasks()
    assert len(tasks) == 1
    assert tasks[0] == created

def test_update_task(client):
    # First create a task
    client.post("/api/tasks", json={"content": "Old", "state": "Por Hacer"})
    # Update it
    response = client.put("/api/tasks/1", json={"content": "New", "state": "En Progreso"})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated["content"] == "New"
    assert updated["state"] == "En Progreso"

    # Check file consistency
    tasks = _read_tasks()
    assert tasks[0]["content"] == "New"
    assert tasks[0]["state"] == "En Progreso"

def test_delete_task(client):
    client.post("/api/tasks", json={"content": "To delete"})
    response = client.delete("/api/tasks/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted" in data["message"]

    tasks = _read_tasks()
    assert len(tasks) == 0

# Edge cases

def test_create_missing_content(client):
    response = client.post("/api/tasks", json={})
    assert response.status_code == 400

def test_update_nonexistent(client):
    response = client.put("/api/tasks/999", json={"content": "X"})
    assert response.status_code == 404

def test_delete_nonexistent(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
