import json

import pytest

from backend import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c

@pytest.fixture(autouse=True)
def patch_tasks_file(monkeypatch, tmp_path):
    # Redirect the TASKS_FILE used in routes to a temporary file.
    monkeypatch.setattr('backend.routes.TASKS_FILE', tmp_path / 'tasks.json')

def test_crud_operations(client):
    # 1. Create a new task
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    created_task = response.get_json()

    # Verify fields
    assert created_task['id'] == 1
    assert created_task['content'] == 'Test Task'
    assert created_task['state'] == 'Por Hacer'

    # 2. Retrieve all tasks
    response = client.get('/api/tasks')
    assert response.status_code == 200
    tasks_list = response.get_json()
    assert isinstance(tasks_list, list)
    assert len(tasks_list) == 1

    # 3. Update the task
    update_data = {'content': 'Updated Task', 'state': 'En Progreso'}
    response = client.put(f'/api/tasks/{created_task['id']}', json=update_data)
    assert response.status_code == 200
    updated_task = response.get_json()

    assert updated_task['content'] == 'Updated Task'
    assert updated_task['state'] == 'En Progreso'

    # 4. Delete the task
    response = client.delete(f'/api/tasks/{created_task['id']}')
    assert response.status_code == 204

    # Ensure it is removed
    response = client.get('/api/tasks')
    tasks_list = response.get_json()
    assert len(tasks_list) == 0

def test_404_on_nonexistent_task(client):
    response = client.put('/api/tasks/999', json={'content': 'Nope'})
    assert response.status_code == 404

    response = client.delete('/api/tasks/999')
    assert response.status_code == 404