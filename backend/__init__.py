from flask import Flask, Blueprint, request, jsonify, send_from_directory, current_app

# Factory to create the Flask app
def create_app():
    """Create and configure a Flask application instance."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Root route to serve the frontend index.html
    @app.route('/')
    def root():
        return send_from_directory(app.static_folder, 'index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    return app