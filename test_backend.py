import json
import os
import pytest
from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path):
    file = tmp_path / 'tasks.json'
    # Redirect the global variable during tests
    original = TASKS_FILE
    try:
        globals()['TASKS_FILE'] = str(file)
        if not file.exists():
            file.write_text('[]')
        yield file
    finally:
        globals()['TASKS_FILE'] = original

def test_delete_existing_task(client, temp_tasks_file):
    # Create a task first
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    data = response.get_json()
    task_id = data['id']
    # Delete the task
    del_resp = client.delete(f'/api/tasks/{task_id}')
    assert del_resp.status_code == 204
    # Verify it's gone
    get_resp = client.get('/api/tasks')
    tasks = get_resp.get_json()
    assert all(t['id'] != task_id for t in tasks)

def test_delete_nonexistent_task(client, temp_tasks_file):
    resp = client.delete('/api/tasks/9999')
    assert resp.status_code == 404
    err = resp.get_json()
    assert 'error' in err
