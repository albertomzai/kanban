# sitecustomize.py – ejecutado automáticamente al iniciar Python
import werkzeug

if not hasattr(werkzeug, "__version__"):
    # Proporciona el atributo esperado por Flask testing
    werkzeug.__version__ = "0"