import pytest
from backend import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

# Helper to create a task for testing delete

def create_test_task(client):
    response = client.post('/api/tasks', json={'content': 'Test Task'})
    assert response.status_code == 201
    return response.get_json()['id']

def test_delete_existing_task(client):
    task_id = create_test_task(client)
    delete_resp = client.delete(f'/api/tasks/{task_id}')
    assert delete_resp.status_code == 200
    # Verify it's gone
    get_resp = client.get('/api/tasks')
    tasks = get_resp.get_json()
    ids = [t['id'] for t in tasks]
    assert task_id not in ids

def test_delete_nonexistent_task(client):
    delete_resp = client.delete('/api/tasks/nonexistent-id')
    assert delete_resp.status_code == 404