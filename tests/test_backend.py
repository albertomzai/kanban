# -*- coding: utf-8 -*-
"""
Unit tests for the Kanban API.

The tests use Flask's test client and monkeypatch to isolate file I/O.
"""

import json
from pathlib import Path
import pytest
from backend import app as flask_app, TASKS_FILE

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    with flask_app.test_client() as c:
        yield c

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    """Redirect the global TASKS_FILE to a temporary file.

    This ensures that tests do not touch the real ``tasks.json``.
    """
    tmp = tmp_path / "tasks.json"
    monkeypatch.setattr("backend.TASKS_FILE", str(tmp))
    # Ensure the file exists before each test
    tmp.write_text("[]")
    return tmp

# ---------------------------------------------------------------------------
# Helper to parse JSON response
# ---------------------------------------------------------------------------
def _json_response(resp):
    return json.loads(resp.data.decode("utf-8"))

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
def test_get_tasks_empty(client, temp_tasks_file):
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    data = _json_response(resp)
    assert "tasks" in data and isinstance(data["tasks"], list) and len(data["tasks"]) == 0

def test_create_task(client, temp_tasks_file):
    payload = {"content": "Test task", "state": "Por Hacer"}
    resp = client.post("/api/tasks", json=payload)
    assert resp.status_code == 201
    data = _json_response(resp)
    assert data["id"] == 1
    assert data["content"] == payload["content"]
    assert data["state"] == payload["state"]

    # Verify persistence
    resp2 = client.get("/api/tasks")
    data2 = _json_response(resp2)
    assert len(data2["tasks"]) == 1

def test_update_task(client, temp_tasks_file):
    # Create a task first
    client.post("/api/tasks", json={"content": "Old", "state": "Por Hacer"})
    # Update it
    resp = client.put("/api/tasks/1", json={"content": "New", "state": "En Progreso"})
    assert resp.status_code == 200
    data = _json_response(resp)
    assert data["content"] == "New"
    assert data["state"] == "En Progreso"

def test_delete_task(client, temp_tasks_file):
    client.post("/api/tasks", json={"content": "To delete", "state": "Por Hacer"})
    resp = client.delete("/api/tasks/1")
    assert resp.status_code == 200
    data = _json_response(resp)
    assert data["message"] == "Task deleted successfully."
    # Verify deletion
    resp2 = client.get("/api/tasks")
    tasks = _json_response(resp2)["tasks"]
    assert len(tasks) == 0
