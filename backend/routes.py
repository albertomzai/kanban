#!/usr/bin/env python3
from flask import Blueprint, request, jsonify
from backend import db

api = Blueprint('api', __name__)

def get_tasks():
    return jsonify(db.get_tasks())  # obtener todas las tareas

def add_task():
    task = request.json
    db.add_task(task)
    return jsonify({'message': 'Task created'})

def update_task(id):
    task = request.json
    db.update_task(task, id)
    return jsonify({'message': 'Task updated'})

def delete_task(id):
    db.delete_task(id)
    return jsonify({'message': 'Task deleted'})

api.route('/tasks', methods=['GET'])(get_tasks)
api.route('/tasks', methods=['POST'])(add_task)
api.route('/tasks/<int:id>', methods=['PUT'])(update_task)
api.route('/tasks/<int:id>', methods=['DELETE'])(delete_task)