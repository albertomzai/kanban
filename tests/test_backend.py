import pytest
from backend import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_delete_task(client, monkeypatch, tmp_path):
    # Setup: create a task file
    tasks_file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.TASKS_FILE', str(tasks_file))
    # Create a sample task
    sample_task = {'id': 1, 'content': 'Test task', 'state': 'Por Hacer'}
    with open(tasks_file, 'w') as f:
        json.dump([sample_task], f)
    # Perform DELETE request
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # Verify file is empty
    with open(tasks_file) as f:
        data = json.load(f)
    assert data == []
