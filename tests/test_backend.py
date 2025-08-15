import json

import pytest

from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_tasks_file(tmp_path, monkeypatch):
    # Redirect TASKS_FILE to a temporary file for each test
    temp_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.TASKS_FILE', str(temp_file))

@pytest.fixture
def empty_tasks():
    return []

def test_get_empty(client, empty_tasks):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert data == empty_tasks

def test_create_task(client):
    payload = {'content': 'Test task', 'state': 'Por Hacer'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == payload['content']
    assert data['state'] == payload['state']

def test_update_task(client):
    # First create a task
    client.post('/api/tasks', json={'content': 'Old', 'state': 'Por Hacer'})
    # Update it
    update_payload = {'content': 'Updated', 'state': 'En Progreso'}
    response = client.put('/api/tasks/1', json=update_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == update_payload['content']
    assert data['state'] == update_payload['state']

def test_delete_task(client):
    # Create a task to delete
    client.post('/api/tasks', json={'content': 'To be deleted'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {}

def test_nonexistent_update(client):
    response = client.put('/api/tasks/999', json={'content': 'X'})
    assert response.status_code == 404

def test_nonexistent_delete(client):
    response = client.delete('/api/tasks/999')
    assert response.status_code == 404