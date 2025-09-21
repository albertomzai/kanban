import pytest
from backend import create_app as flask_app

@pytest.fixture
def client():
    app = flask_app()
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert isinstance(response.json, list)

@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.routes.TASKS_FILE', str(file))
    return file

def test_create_task(client, temp_file):
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    assert response.json['content'] == 'Test Task'
    assert response.json['state'] == 'Por Hacer'
    assert temp_file.exists() and temp_file.read_text().strip() != ''

def test_update_task(client, temp_file):
    client.post('/api/tasks', json={'content': 'Test Task'})
    response = client.put('/api/tasks/1', json={'state': 'En Progreso'})
    assert response.status_code == 200
    assert response.json['state'] == 'En Progreso'

def test_delete_task(client, temp_file):
    client.post('/api/tasks', json={'content': 'Test Task'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    assert not any(task['id'] == 1 for task in json.loads(temp_file.read_text()))