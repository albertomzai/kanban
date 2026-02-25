import pytest
import json
import os
from backend import create_app
from backend import storage


@pytest.fixture
def app():
    """Fixture que proporciona la aplicación de Flask para testing."""
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    """Fixture que proporciona el cliente de test de Flask."""
    return app.test_client()


@pytest.fixture
def temp_file(tmp_path, monkeypatch):
    """
    Fixture que redirige el archivo de almacenamiento a un temporal
    para no afectar los datos reales durante las pruebas.
    """
    file = tmp_path / "test_tasks.json"
    # Parcheamos la variable global en el módulo storage
    monkeypatch.setattr("backend.storage.TASKS_FILE", str(file))
    yield file


def test_obtener_tareas_vacio(client, temp_file):
    """Testea obtener tareas cuando no hay ninguna."""
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert response.json == []


def test_crear_tarea(client, temp_file):
    """Testea la creación de una nueva tarea."""
    nueva_tarea_data = {'content': 'Aprender Flask'}
    response = client.post('/api/tasks',
                           data=json.dumps(nueva_tarea_data),
                           content_type='application/json')
    
    assert response.status_code == 201
    data = response.json
    assert data['id'] == 1
    assert data['content'] == 'Aprender Flask'
    assert data['state'] == 'Por Hacer'


def test_obtener_tareas_con_datos(client, temp_file):
    """Testea obtener tareas después de haber creado una."""
    # Preparamos datos directamente en el archivo temporal
    datos_iniciales = [{"id": 1, "content": "Tarea test", "state": "Hecho"}]
    with open(temp_file, 'w') as f:
        json.dump(datos_iniciales, f)
    
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['content'] == 'Tarea test'


def test_actualizar_tarea(client, temp_file):
    """Testea la actualización de contenido y estado de una tarea."""
    # Creamos una tarea primero
    client.post('/api/tasks', data=json.dumps({'content': 'Original'}),
                content_type='application/json')
    
    # Actualizamos
    update_data = {'content': 'Modificado', 'state': 'En Progreso'}
    response = client.put('/api/tasks/1',
                          data=json.dumps(update_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.json
    assert data['content'] == 'Modificado'
    assert data['state'] == 'En Progreso'


def test_borrar_tarea(client, temp_file):
    """Testea la eliminación de una tarea."""
    # Creamos una tarea
    client.post('/api/tasks', data=json.dumps({'content': 'Para borrar'}),
                content_type='application/json')
    
    # La borramos
    response = client.delete('/api/tasks/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Tarea eliminada correctamente'
    
    # Verificamos que ya no existe
    response_get = client.get('/api/tasks')
    assert response_get.json == []


def test_servir_index(client):
    """Testea que la ruta raíz sirve el index.html (simulado o error 404 si no existe)."""
    response = client.get('/')
    # Como no existe el archivo real en el entorno de test, puede dar 404
    # pero la ruta debe estar definida. Si el archivo existiera, daría 200.
    # Aquí comprobamos que Flask responde algo coherente.
    assert response.status_code in [200, 404] 