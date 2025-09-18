"""Entry point for running the Flask application."""

from backend import create_app

app = create_app()

if __name__ == '__main__':
    # Run in debug mode when executed directly
    app.run(debug=True)