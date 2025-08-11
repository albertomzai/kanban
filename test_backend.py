import pytest
from backend import app as flask_app, TASKS_FILE
import json
import os

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    file = tmp_path / "tasks.json"
    # Ensure the file exists for load_tasks to read
    file.write_text("[]")
    monkeypatch.setattr('backend.TASKS_FILE', str(file))
    return file

def test_delete_existing_task(client, temp_tasks_file):
    # Create a task first
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    task_id = data['id']
    # Delete the task
    del_response = client.delete(f'/api/tasks/{task_id}')
    assert del_response.status_code == 204
    # Verify it's removed
    get_resp = client.get('/api/tasks')
    tasks = get_resp.get_json()
    assert all(t['id'] != task_id for t in tasks)

def test_delete_nonexistent_task(client, temp_tasks_file):
    response = client.delete('/api/tasks/9999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data