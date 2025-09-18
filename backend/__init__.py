# backend/__init__.py

import os
from flask import Flask, Blueprint

tasks_bp = Blueprint('tasks_bp', __name__)

def create_app() -> Flask:
    """Factory function that creates and configures the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the tasks blueprint
    from . import routes  # noqa: F401
    app.register_blueprint(tasks_bp)

    return app