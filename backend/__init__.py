import os

from flask import Flask, send_from_directory

def create_app():
    """Factory function to create and configure the Flask application."""

    # The static folder is one level up in the frontend directory.
    app = Flask(__name__, static_folder=os.path.join(os.pardir, 'frontend'), static_url_path='')

    # Register API blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        """Serve the main frontend page."""
        return send_from_directory(app.static_folder, 'index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad request"}, 400

    return app