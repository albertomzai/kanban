"""
Package initializer for the backend module.
Exposes the Flask application instance so that tests can import it via
`from backend import app`.
"""
# Import the Flask app from the submodule
from .app import app
