"""Unit tests for the Kanban backend API."""

import json
from pathlib import Path

import pytest

# Import the factory and constants to be used in tests
from backend import create_app
from backend.routes import TASKS_FILE, VALID_STATES

@pytest.fixture
def app():
    """Create a fresh Flask test client for each test."""
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    """Redirect TASKS_FILE to a temporary file for isolation."""
    temp = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.routes.TASKS_FILE', temp)
    return temp

@pytest.fixture(autouse=True)
def clean_tasks_file(temp_file):
    # Ensure the file is empty before each test
    if temp_file.exists():
        temp_file.unlink()

def test_get_empty(client, temp_file):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_create_task(client, temp_file):
    payload = {'content': 'Test task'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == 'Test task'
    assert data['state'] == 'Por Hacer'

def test_update_task(client, temp_file):
    # First create a task
    client.post('/api/tasks', json={'content': 'Old'})
    # Update it
    update = {'content': 'New', 'state': 'En Progreso'}
    response = client.put('/api/tasks/1', json=update)
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'New'
    assert data['state'] == 'En Progreso'

def test_delete_task(client, temp_file):
    client.post('/api/tasks', json={'content': 'To delete'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # Verify removal
    get_resp = client.get('/api/tasks')
    assert get_resp.json == []