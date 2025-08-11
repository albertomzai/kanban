# Top-level entry point for the backend package
# This module imports and re‑exports the Flask application instance
# and the TASKS_FILE path defined in backend.app.

from backend.app import app, TASKS_FILE
__all__ = ["app", "TASKS_FILE"]