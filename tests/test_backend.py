import os
import json
import pytest

from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

# Helper to reset tasks.json before each test
@pytest.fixture(autouse=True)
def clear_tasks_file(tmp_path, monkeypatch):
    file_path = tmp_path / 'tasks.json'
    # Patch the TASKS_FILE path in routes module
    import backend.routes as routes
    monkeypatch.setattr(routes, 'TASKS_FILE', file_path)

    # Ensure file is empty before test
    if file_path.exists():
        file_path.unlink()

    yield

def test_get_tasks_empty(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_task(client):
    payload = {'content': 'Test task'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == 'Test task'
    assert data['state'] == 'Por Hacer'

def test_update_task(client):
    # First create a task
    client.post('/api/tasks', json={'content': 'Old'})
    # Update it
    response = client.put('/api/tasks/1', json={'content': 'New', 'state': 'En Progreso'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'New'
    assert data['state'] == 'En Progreso'

def test_delete_task(client):
    client.post('/api/tasks', json={'content': 'To delete'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # Verify deletion
    get_resp = client.get('/api/tasks')
    assert get_resp.get_json() == []