import json
import os
from backend import app as flask_app, TASKS_FILE

# Fixture for test client
@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Helper to set up a temporary tasks file via monkeypatch
@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    file = tmp_path / "test_tasks.json"
    # Redirect TASKS_FILE during the test
    monkeypatch.setattr("backend.TASKS_FILE", file)
    return file

# Ensure that DELETE returns 204 when task exists
def test_delete_existing_task(client, temp_tasks_file):
    # Prepare a task in the temporary file
    tasks = [{"id": 1, "content": "Test", "status": "Por Hacer"}]
    with open(temp_tasks_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f)

    response = client.delete("/api/tasks/1")
    assert response.status_code == 204
    # File should now be empty list
    with open(temp_tasks_file, 'r', encoding='utf-8') as f:
        remaining = json.load(f)
    assert remaining == []

# Ensure that DELETE returns 404 when task does not exist
def test_delete_nonexistent_task(client, temp_tasks_file):
    # Empty tasks file
    with open(temp_tasks_file, 'w', encoding='utf-8') as f:
        json.dump([], f)

    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Task not found"
