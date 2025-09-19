"""Integration tests for the backend API."""

import json
from pathlib import Path

import pytest

from backend import create_app

@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    """Create a temporary tasks.json and patch the module constant."""
    file = tmp_path / "tasks.json"
    # Ensure the file exists so that load returns [] rather than raising FileNotFoundError
    file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr("backend.routes.TASKS_FILE", str(file))
    return file

def test_get_tasks_empty(client, temp_tasks_file):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data == []

def test_create_task(client, temp_tasks_file):
    payload = {"content": "Test task", "state": "Por Hacer"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    task = response.get_json()
    assert task["id"] == 1
    assert task["content"] == "Test task"

def test_update_task(client, temp_tasks_file):
    # First create a task
    client.post("/api/tasks", json={"content": "To update", "state": "Por Hacer"})
    # Update it
    response = client.put("/api/tasks/1", json={"content": "Updated", "state": "En Progreso"})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated["content"] == "Updated"
    assert updated["state"] == "En Progreso"

def test_delete_task(client, temp_tasks_file):
    client.post("/api/tasks", json={"content": "To delete", "state": "Por Hacer"})
    response = client.delete("/api/tasks/1")
    assert response.status_code == 204

def test_invalid_create(client, temp_tasks_file):
    # Missing content
    response = client.post("/api/tasks", json={"state": "Por Hacer"})
    assert response.status_code == 400

def test_nonexistent_update(client, temp_tasks_file):
    response = client.put("/api/tasks/999", json={"content": "Does not exist"})
    assert response.status_code == 404