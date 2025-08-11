import pytest
from backend import app as flask_app, TASKS_FILE
import json
import os

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup(tmp_path):
    # Redirect TASKS_FILE to a temp file during tests
    tmp_file = tmp_path / 'tasks.json'
    original = TASKS_FILE
    try:
        globals()['TASKS_FILE'] = str(tmp_file)
        yield
    finally:
        globals()['TASKS_FILE'] = original
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

def test_create_and_get_task(client):
    # Create a task
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['status'] == 'Por Hacer'

    # Get all tasks
    response = client.get('/api/tasks')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]['content'] == 'Test Task'

def test_update_task(client):
    # Create a task first
    client.post('/api/tasks', json={'content': 'Old Content'})
    # Update it
    response = client.put('/api/tasks/1', json={'content': 'New Content', 'status': 'En Progreso'})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated['content'] == 'New Content'
    assert updated['status'] == 'En Progreso'

def test_delete_task(client):
    # Create a task first
    client.post('/api/tasks', json={'content': 'To be deleted'})
    # Delete it
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # Verify deletion
    response = client.get('/api/tasks')
    tasks = response.get_json()
    assert len(tasks) == 0