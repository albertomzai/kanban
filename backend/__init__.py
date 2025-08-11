"""Paquete backend que expone la aplicación Flask y la ruta al archivo de tareas."""

from .app import app, TASKS_FILE

__all__ = ["app", "TASKS_FILE"]
