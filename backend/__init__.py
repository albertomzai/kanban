from flask import Flask, send_static_file
from .routes import api_bp


def create_app():
    """
    Fábrica de aplicaciones para crear y configurar la instancia de Flask.
    Configura la carpeta de archivos estáticos para servir el frontend.
    """
    # Configuración para servir el frontend desde la carpeta '../frontend'
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Registro del Blueprint de la API
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        """
        Ruta raíz que sirve el archivo index.html de la carpeta estática.
        """
        return send_static_file('index.html')

    return app