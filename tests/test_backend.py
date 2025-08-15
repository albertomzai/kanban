import os
import json

import pytest

from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_tasks_file(tmp_path, monkeypatch):
    # Redirect the TASKS_FILE path to a temporary file for each test
    temp_file = tmp_path / "tasks.json"
    monkeypatch.setattr("backend.routes.TASKS_FILE", str(temp_file))

    yield

    # Cleanup after tests
    if temp_file.exists():
        temp_file.unlink()

def test_get_tasks_empty(client):
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_create_task(client):
    payload = {"content": "Test task"}
    resp = client.post("/api/tasks", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["id"] == 1
    assert data["content"] == "Test task"
    assert data["state"] == "Por Hacer"

def test_update_task(client):
    # First create a task
    client.post("/api/tasks", json={"content": "Initial"})
    # Update it
    resp = client.put("/api/tasks/1", json={"content": "Updated", "state": "En Progreso"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["content"] == "Updated"
    assert data["state"] == "En Progreso"

def test_delete_task(client):
    # Create and then delete
    client.post("/api/tasks", json={"content": "To be deleted"})
    resp = client.delete("/api/tasks/1")
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "Deleted successfully"}

def test_get_tasks_after_operations(client):
    # Create two tasks
    client.post("/api/tasks", json={"content": "A"})
    client.post("/api/tasks", json={"content": "B"})
    resp = client.get("/api/tasks")
    data = resp.get_json()
    assert len(data) == 2
    ids = {t["id"] for t in data}
    assert ids == {1, 2}