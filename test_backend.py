import json
import os
import tempfile
from backend import app as flask_app, TASKS_FILE
import pytest

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Helper to set up a temporary tasks file for tests
@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    test_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.TASKS_FILE', str(test_file))
    # Ensure the file starts empty
    if test_file.exists():
        test_file.unlink()
    return test_file

def create_sample_task(client, content='Sample', state='Por Hacer'):
    response = client.post('/api/tasks', json={'content': content, 'state': state})
    assert response.status_code == 201
    return response.get_json()['id']

def test_delete_existing_task(client, temp_tasks_file):
    # Create a task to delete
    task_id = create_sample_task(client)
    # Ensure it exists
    resp = client.get('/api/tasks')
    tasks = resp.get_json()
    assert any(t['id'] == task_id for t in tasks)
    # Delete the task
    del_resp = client.delete(f'/api/tasks/{task_id}')
    assert del_resp.status_code == 204
    # Verify it's removed
    resp_after = client.get('/api/tasks')
    tasks_after = resp_after.get_json()
    assert not any(t['id'] == task_id for t in tasks_after)

def test_delete_nonexistent_task(client, temp_tasks_file):
    # Attempt to delete a non‑existing ID
    del_resp = client.delete('/api/tasks/9999')
    assert del_resp.status_code == 404
    data = del_resp.get_json()
    assert 'error' in data and data['error'] == 'Task not found'
