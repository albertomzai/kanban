import os

from flask import Flask, send_from_directory


def create_app() -> Flask:
    """Factory que crea y configura la aplicación Flask."""

    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'), static_url_path='')

    # Blueprint de la API
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def serve_index():
        """Sirve el archivo index.html del frontend."""
        return send_from_directory(app.static_folder, 'index.html')

    # Manejo de errores genéricos
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not Found"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad Request"}, 400

    return app