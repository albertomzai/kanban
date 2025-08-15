import os

from flask import Flask

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register API blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app