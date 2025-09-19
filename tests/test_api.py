import json

import pytest
from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_get_tasks_empty(client):
    # Ensure GET returns empty list initially
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)

def test_create_and_get_task(client):
    # Create a new task
    payload = {"content": "Test Task"}
    resp = client.post("/api/tasks", json=payload)
    assert resp.status_code == 201
    created = json.loads(resp.data)

    # Retrieve all tasks and check presence
    resp2 = client.get("/api/tasks")
    data = json.loads(resp2.data)
    assert any(t["id"] == created["id"] for t in data)

def test_update_task(client):
    # Create a task first
    resp = client.post("/api/tasks", json={"content": "Update Me"})
    task = json.loads(resp.data)

    # Update its content and state
    update_payload = {"content": "Updated", "state": "En Progreso"}
    resp2 = client.put(f"/api/tasks/{task['id']}", json=update_payload)
    assert resp2.status_code == 200
    updated = json.loads(resp2.data)
    assert updated["content"] == "Updated"
    assert updated["state"] == "En Progreso"

def test_delete_task(client):
    # Create a task to delete
    resp = client.post("/api/tasks", json={"content": "Delete Me"})
    task = json.loads(resp.data)

    resp2 = client.delete(f"/api/tasks/{task['id']}")
    assert resp2.status_code == 200
    msg = json.loads(resp2.data)
    assert "deleted" in msg["message"]