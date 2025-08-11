# test_backend.py
import pytest
from backend import app as flask_app
from tasks import load_tasks, save_tasks, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    file = tmp_path / "tasks.json"
    monkeypatch.setattr("tasks.TASKS_FILE", file)
    # Ensure the file starts empty
    if file.exists():
        file.unlink()
    yield file

def test_delete_existing_task(client, temp_file):
    # Setup: create a task directly in the file
    save_tasks([{'id': 1, 'content': 'Test', 'state': 'Por Hacer'}])
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # Verify file is now empty
    tasks_after = load_tasks()
    assert tasks_after == []

def test_delete_nonexistent_task(client, temp_file):
    # No tasks in file
    response = client.delete('/api/tasks/999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Task not found'