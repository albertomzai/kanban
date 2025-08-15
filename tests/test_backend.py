import json

import pytest

from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    """Provide a temporary tasks.json file for each test."""
    temp_file = tmp_path / 'tasks.json'
    # Ensure the file starts empty.
    temp_file.write_text('[]', encoding='utf-8')
    monkeypatch.setattr("backend.routes.TASKS_FILE", temp_file)
    return temp_file

def test_get_tasks_empty(client, temp_tasks_file):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data == []

def test_create_task(client, temp_tasks_file):
    payload = {'content': 'Test task', 'state': 'Por Hacer'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == payload['content']
    assert data['state'] == payload['state']

def test_update_task(client, temp_tasks_file):
    # First create a task to update.
    client.post('/api/tasks', json={'content': 'Old content'})
    # Update the task.
    response = client.put('/api/tasks/1', json={'content': 'New content', 'state': 'En Progreso'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'New content'
    assert data['state'] == 'En Progreso'

def test_delete_task(client, temp_tasks_file):
    # Create a task to delete.
    client.post('/api/tasks', json={'content': 'To be deleted'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {}

    # Verify it no longer exists.
    get_response = client.get('/api/tasks')
    assert get_response.status_code == 200
    tasks = get_response.get_json()
    assert len(tasks) == 0