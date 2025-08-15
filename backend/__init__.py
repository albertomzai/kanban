from flask import Flask

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Serve the frontend index.html file."""
        return app.send_static_file('index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(400)
    def bad_request(error):
        return {'error': str(error)}, 400

    return app