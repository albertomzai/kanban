import json
import os
import pytest
from backend import app as flask_app, TASKS_FILE

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    file = tmp_path / "tasks.json"
    # Parchar la ruta del archivo de tareas para usar el temporal
    monkeypatch.setattr("backend.TASKS_FILE", str(file))
    return file

# Helper to write initial tasks

def write_tasks(file, tasks):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f)

def test_delete_existing_task(client, temp_tasks_file):
    # Arrange: crear dos tareas
    initial = [
        {'id': 1, 'content': 'Task One', 'status': 'Por Hacer'},
        {'id': 2, 'content': 'Task Two', 'status': 'En Progreso'}
    ]
    write_tasks(temp_tasks_file, initial)

    # Act: eliminar la tarea con id=1
    response = client.delete("/api/tasks/1")

    # Assert
    assert response.status_code == 204
    # Verificar que solo quede la segunda tarea
    with open(temp_tasks_file) as f:
        remaining = json.load(f)
    assert len(remaining) == 1
    assert remaining[0]['id'] == 2

def test_delete_nonexistent_task(client, temp_tasks_file):
    # Arrange: archivo vacío
    write_tasks(temp_tasks_file, [])

    # Act: intentar eliminar id que no existe
    response = client.delete("/api/tasks/999")

    # Assert
    assert response.status_code == 404
