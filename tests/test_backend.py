# tests/test_backend.py

import json
import os
import pytest

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_tasks_file(tmp_path, monkeypatch):
    # Ensure a fresh tasks.json for each test run
    file_path = tmp_path / 'tasks.json'
    monkeypatch.setenv('TASKS_FILE', str(file_path))
    # Monkeypatch the internal path used in routes
    from backend import routes
    routes._TASKS_FILE = str(file_path)

def test_get_tasks_empty(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) and len(data) == 0

def test_create_task(client):
    payload = {'content': 'Test task'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == 'Test task'

def test_update_task(client):
    # First create a task
    client.post('/api/tasks', json={'content': 'Old content'})
    # Update it
    response = client.put('/api/tasks/1', json={'content': 'New content', 'status': 'En Progreso'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'New content'
    assert data['status'] == 'En Progreso'

def test_delete_task(client):
    client.post('/api/tasks', json={'content': 'To delete'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Task deleted.'

def test_not_found(client):
    response = client.put('/api/tasks/999', json={'content': 'X'})
    assert response.status_code == 404

def test_bad_request(client):
    # Missing content on create
    response = client.post('/api/tasks', json={})
    assert response.status_code == 400