import json
import os
from pathlib import Path

import pytest

# Import the Flask app factory
from backend import create_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Ensure a clean tasks.json for each test run
    tasks_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.tasks._TASKS_FILE', tasks_file)

    app = create_app()
    with app.test_client() as c:
        yield c

def test_get_tasks_empty(client):
    resp = client.get('/api/tasks')
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_create_task(client):
    payload = {'content': 'Test task'}
    resp = client.post('/api/tasks', json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['id'] == 1
    assert data['content'] == 'Test task'
    assert data['status'] == 'Por Hacer'

def test_update_task(client):
    # First create a task
    client.post('/api/tasks', json={'content': 'Old'})
    # Update it
    resp = client.put('/api/tasks/1', json={'content': 'New', 'status': 'Hecho'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['content'] == 'New'
    assert data['status'] == 'Hecho'

def test_delete_task(client):
    client.post('/api/tasks', json={'content': 'To delete'})
    resp = client.delete('/api/tasks/1')
    assert resp.status_code == 200
    assert resp.get_json() == {'message': 'Deleted'}

def test_task_not_found(client):
    resp = client.put('/api/tasks/999', json={'content': 'Does not exist'})
    assert resp.status_code == 404

    resp = client.delete('/api/tasks/999')
    assert resp.status_code == 404