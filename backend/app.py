from flask import Flask

from backend.routes import api_bp

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the API blueprint
    app.register_blueprint(api_bp)

    return app