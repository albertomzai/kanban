"""Flask application factory for the Kanban backend."""

import os
from flask import Flask
from flask_cors import CORS

# Import the blueprint that contains all API routes
from .routes import tasks_bp

def create_app() -> Flask:
    """Create and configure a new Flask application instance."""

    # The static folder is one level up in the frontend directory.
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Enable CORS for all routes (useful for local development)
    CORS(app)

    # Register the tasks blueprint under /api prefix
    app.register_blueprint(tasks_bp, url_prefix='/api')

    @app.route('/')
    def index():  # pragma: no cover - served automatically by Flask static
        """Serve the frontend index.html file."""
        return app.send_static_file('index.html')

    return app