import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Ruta al archivo de tareas dentro del paquete
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))
CORS(app)

# ---------------------------------------------------------------------------
# Helpers para leer y escribir tareas
# ---------------------------------------------------------------------------

def _load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# Rutas de la API RESTful
# ---------------------------------------------------------------------------
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(_load_tasks()), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    content = data.get("content")
    if not content:
        return jsonify({"error": "Content required"}), 400
    tasks = _load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id": new_id, "content": content, "status": "Por Hacer"}
    tasks.append(new_task)
    _save_tasks(tasks)
    return jsonify(new_task), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(force=True)
    tasks = _load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t.update({k: v for k, v in data.items() if k in ["content", "status"]})
            _save_tasks(tasks)
            return jsonify(t), 200
    return jsonify({"error": "Task not found"}), 404

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = _load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({"error": "Task not found"}), 404
    _save_tasks(new_tasks)
    return jsonify({"message": "Task deleted"}), 200

# ---------------------------------------------------------------------------
# Ruta para servir el frontend (index.html)
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")
