from backend import create_app


__name__ = "__main__"

if __name__ == "__main__":
    app = create_app()
    # Ejecutar la aplicación en modo desarrollo
    app.run(host="0.0.0.0", port=5000, debug=True)