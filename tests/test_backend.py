import json
from pathlib import Path

import pytest


@pytest.fixture
def client():
    from backend import create_app
    app = create_app()
    with app.test_client() as c:
        yield c


@pytest.fixture
def temp_tasks_file(tmp_path, monkeypatch):
    """Crea un archivo temporal para las tareas y parchea TASKS_FILE."""
    file = tmp_path / 'tasks.json'
    monkeypatch.setattr('backend.routes.TASKS_FILE', str(file))
    return file

@pytest.fixture(autouse=True)
def clean_tasks_file(temp_tasks_file):
    # Garantiza que el archivo comience vacío antes de cada test
    temp_tasks_file.write_text('[]')


def test_get_empty(client, temp_tasks_file):
    response = client.get('/api/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert data == []

def test_create_task(client, temp_tasks_file):
    payload = {'content': 'Nueva tarea'}
    response = client.post('/api/tasks', json=payload)
    assert response.status_code == 201
    task = response.get_json()
    assert task['id'] == 1
    assert task['content'] == payload['content']
    assert task['status'] == 'Por Hacer'

    # Verifica que el archivo contiene la tarea
    stored = json.loads(temp_tasks_file.read_text())
    assert len(stored) == 1
    assert stored[0]['id'] == 1

def test_update_task(client, temp_tasks_file):
    # Primero crear una tarea
    client.post('/api/tasks', json={'content': 'Tarea'})

    # Actualizarla
    response = client.put('/api/tasks/1', json={'status': 'En Progreso', 'content': 'Actualizada'})
    assert response.status_code == 200
    updated = response.get_json()
    assert updated['status'] == 'En Progreso'
    assert updated['content'] == 'Actualizada'

def test_delete_task(client, temp_tasks_file):
    client.post('/api/tasks', json={'content': 'Eliminar'})
    response = client.delete('/api/tasks/1')
    assert response.status_code == 204
    # Verifica que el archivo está vacío
    stored = json.loads(temp_tasks_file.read_text())
    assert stored == []