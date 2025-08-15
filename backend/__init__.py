import os

from flask import Flask

def create_app() -> Flask:
    """Create and configure a new Flask application instance."""
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'), static_url_path='')

    # Register the tasks blueprint
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp)

    return app

# Create a default app instance for testing and convenience.
app = create_app()