# app.py - entry point for running the Flask application

from backend import create_app

__name__ == "__main__" and create_app().run(debug=True)