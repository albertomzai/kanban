import pytest
from backend import app as flask_app
import os
import json

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Helper to reset tasks file before each test
TASKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'backend', 'tasks.json')

@pytest.fixture(autouse=True)
def reset_tasks_file(tmp_path, monkeypatch):
    # Create a temporary tasks.json for isolation
    temp_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.app.TASKS_FILE', str(temp_file))
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump([], f)
    yield

def test_create_and_delete_task(client):
    # Create a task
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    task_id = data['id']

    # Verify it exists via GET
    get_resp = client.get('/api/tasks')
    tasks = get_resp.get_json()
    assert any(t['id'] == task_id for t in tasks)

    # Delete the task
    del_resp = client.delete(f'/api/tasks/{task_id}')
    assert del_resp.status_code == 200
    msg = del_resp.get_json()
    assert msg['message'] == 'Task deleted'

    # Verify it no longer exists
    get_resp_after = client.get('/api/tasks')
    tasks_after = get_resp_after.get_json()
    assert not any(t['id'] == task_id for t in tasks_after)
