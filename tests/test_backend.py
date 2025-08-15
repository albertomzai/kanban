import json

import pytest
from backend import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as c:
        yield c

def test_get_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_task(client):
    payload = {"content": "Test task"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Test task"

def test_update_task(client):
    # First create a task to update
    payload = {"content": "Initial"}
    post_resp = client.post("/api/tasks", json=payload)
    task_id = post_resp.get_json()["id"]

    update_payload = {"status": "En Progreso"}
    put_resp = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert put_resp.status_code == 200
    updated_task = put_resp.get_json()
    assert updated_task["status"] == "En Progreso"

def test_delete_task(client):
    # Create a task to delete
    payload = {"content": "To be deleted"}
    post_resp = client.post("/api/tasks", json=payload)
    task_id = post_resp.get_json()["id"]

    del_resp = client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == 200
    # Verify deletion
    get_resp = client.get("/api/tasks")
    tasks = get_resp.get_json()
    assert not any(t["id"] == task_id for t in tasks)