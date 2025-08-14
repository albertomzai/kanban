# backend/__init__.py
from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp)
    return app
