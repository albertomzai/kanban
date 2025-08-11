import json
import os
import pytest
from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    """Provide a temporary tasks.json file for tests.
    The backend module uses the global TASKS_FILE variable; we patch it to point to a temp file.
    """
    tmp_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.TASKS_FILE', str(tmp_file))
    # Ensure the file starts empty
    tmp_file.write_text('[]')
    return tmp_file

def test_create_task(client, temp_tasks_file):
    response = client.post('/api/tasks', json={'content': 'Test task'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 1
    assert data['content'] == 'Test task'
    # Verify persistence
    tasks_in_file = json.loads(temp_tasks_file.read_text())
    assert len(tasks_in_file) == 1
    assert tasks_in_file[0]['content'] == 'Test task'

def test_get_tasks(client, temp_tasks_file):
    # Prepopulate file with two tasks
    temp_tasks_file.write_text(json.dumps([
        {'id': 1, 'content': 'A', 'status': 'Por Hacer'},
        {'id': 2, 'content': 'B', 'status': 'En Progreso'}
    ]))
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_update_task(client, temp_tasks_file):
    temp_tasks_file.write_text(json.dumps([
        {'id': 1, 'content': 'Old', 'status': 'Por Hacer'}
    ]))
    response = client.put('/api/tasks/1', json={'content': 'New', 'status': 'Hecho'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['content'] == 'New'
    assert data['status'] == 'Hecho'

def test_delete_task_success(client, temp_tasks_file):
    temp_tasks_file.write_text(json.dumps([
        {'id': 1, 'content': 'To delete', 'status': 'Por Hacer'}
    ]))
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # File should be empty after deletion
    tasks_after = json.loads(temp_tasks_file.read_text())
    assert tasks_after == []

def test_delete_task_not_found(client, temp_tasks_file):
    temp_tasks_file.write_text(json.dumps([]))
    response = client.delete('/api/tasks/999')
    assert response.status_code == 404
