"""Backend package initialization.

This module exposes the :func:`create_app` factory that builds the Flask
application configured to serve static files from the frontend folder and
registers the tasks blueprint.
"""

from flask import Flask

# Import the Blueprint for task management
from .routes import tasks_bp

def create_app() -> Flask:
    """Create and configure a new Flask application instance.

    The static folder is set to ``../frontend`` relative to this package so
    that the single‑page application can be served directly by the backend.
    """

    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register API blueprint
    app.register_blueprint(tasks_bp, url_prefix="/api")

    @app.route("/")
    def index():  # pragma: no cover - simple redirect to static index.html
        return app.send_static_file("index.html")

    return app