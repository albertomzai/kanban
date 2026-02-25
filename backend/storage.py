import json
import os

# Ruta del archivo donde se persistirán las tareas
TASKS_FILE = 'tasks.json'


def cargar_tareas():
    """
    Lee las tareas desde el archivo JSON.
    Si el archivo no existe o hay un error, devuelve una lista vacía.
    """
    try:
        if not os.path.exists(TASKS_FILE):
            return []
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_tareas(tareas):
    """
    Escribe la lista de tareas en el archivo JSON.
    
    Args:
        tareas (list): Lista de diccionarios representando las tareas.
    """
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tareas, f, indent=4, ensure_ascii=False)