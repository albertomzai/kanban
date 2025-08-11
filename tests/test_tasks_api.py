import json
import pytest
from backend import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Helper to reset tasks file before each test
@pytest.fixture(autouse=True)
def clear_tasks_file(tmp_path, monkeypatch):
    task_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.TASKS_FILE', str(task_file))
    # Ensure the file starts empty
    if task_file.exists():
        task_file.unlink()
    yield
    if task_file.exists():
        task_file.unlink()

def test_create_task(client):
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == 'Test Task'
    assert data['status'] == 'Por Hacer'

def test_get_tasks(client):
    client.post('/api/tasks', json={'content': 'First'})
    client.post('/api/tasks', json={'content': 'Second', 'status': 'En Progreso'})
    response = client.get('/api/tasks')
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 2

def test_update_task(client):
    client.post('/api/tasks', json={'content': 'Old'})
    response = client.put('/api/tasks/1', json={'content': 'New', 'status': 'Hecho'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'New'
    assert data['status'] == 'Hecho'

def test_delete_task(client):
    client.post('/api/tasks', json={'content': 'To be deleted'})
    delete_resp = client.delete('/api/tasks/1')
    assert delete_resp.status_code == 204
    get_resp = client.get('/api/tasks')
    tasks = get_resp.get_json()
    assert len(tasks) == 0