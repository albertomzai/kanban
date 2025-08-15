"""Package backend – factory for the Flask application."""

from flask import Flask, Blueprint

_bp = Blueprint("api", __name__, url_prefix="/api")

def create_app() -> Flask:
    """Create and configure a Flask application instance.

    Returns:
        Flask: The configured Flask app.
    """
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register API blueprint
    from . import routes  # noqa: F401
    app.register_blueprint(routes.api_bp)

    return app