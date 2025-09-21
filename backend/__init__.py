from flask import Flask, jsonify, request, send_from_directory
from .routes import api_bp
import os

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    @app.route('/', methods=['GET'])
    def index():
        return send_from_directory('../frontend', 'index.html')

    app.register_blueprint(api_bp, url_prefix='/api')
    return app