#!/usr/bin/env python3
import pytest
from backend import create_app, get_tasks, add_task, update_task, delete_task
from backend.routes import api as routes

def test_get_tasks():
    # Crear un cliente de Flask que simulará las peticiones
    with create_app().test_client() as client:
        response = client.get("/api/tasks")
        assert response.status_code == 200