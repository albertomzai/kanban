# Mini‑Trello Kanban

## Visión General del Proyecto
Mini‑Trello es una aplicación web ligera que permite gestionar tareas a través de un tablero Kanban con tres columnas: **Por Hacer**, **En Progreso** y **Hecho**.  
El proyecto se divide en dos capas:

* **Frontend** (HTML + Bootstrap + JavaScript puro) sirve la interfaz de usuario, consume la API REST y gestiona eventos de drag‑and‑drop para mover tarjetas entre columnas.
* **Backend** (Flask) expone una API sencilla que persiste las tareas en un archivo JSON local. Se utiliza el patrón *factory* para crear la aplicación y se registra un blueprint con todas las rutas `/api/tasks`.

El flujo típico es:
1. El cliente carga la página, la cual solicita `GET /api/tasks`.
2. El backend devuelve la lista de tareas almacenadas.
3. Los usuarios crean, actualizan o eliminan tareas mediante llamadas POST/PUT/DELETE.
4. Cada acción se refleja inmediatamente en el DOM y se guarda en `tasks.json`.

## Arquitectura del Sistema
```mermaid
graph TD
    A[Cliente (navegador)] -->|HTTP| B[Flask App]
    B --> C{Blueprint tasks}
    C -->|GET/POST/PUT/DELETE| D[tasks_storage.py]
    D --> E[tasks.json (persistencia)]
```

* **Flask App**  
  * `create_app()` configura la app, registra el blueprint y sirve los archivos estáticos de la carpeta `frontend`.
* **Blueprint `tasks_bp`**  
  * Rutas:
    - `GET /api/tasks`
    - `POST /api/tasks`
    - `PUT /api/tasks/<id>`
    - `DELETE /api/tasks/<id>`
* **Persistencia**  
  * `tasks_storage.py` gestiona la lectura/escritura de `tasks.json`. Si el archivo no existe o está corrupto, devuelve una lista vacía.

## Endpoints de la API

| Método | Ruta | Descripción | Parámetros | Respuesta |
|--------|------|-------------|------------|-----------|
| **GET** | `/api/tasks` | Obtener todas las tareas. | Ninguno | `200 OK` con JSON array de tareas. |
| **POST** | `/api/tasks` | Crear una nueva tarea. | Body: `{ "content": "<texto>" }` | `201 Created` con objeto tarea creado. |
| **PUT** | `/api/tasks/<int:id>` | Actualizar contenido o estado de una tarea existente. | Body opcional: `{ "content": "...", "state": "..." }` | `200 OK` con tarea actualizada. |
| **DELETE** | `/api/tasks/<int:id>` | Eliminar una tarea por id. | Ninguno | `204 No Content`. |

### Ejemplo de respuesta
```json
{
  "id": 3,
  "content": "Revisar PR",
  "state": "En Progreso"
}
```

## Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tuusuario/minitrello.git
   cd minitrello
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install Flask
   ```

4. **Ejecutar la aplicación**  
   ```bash
   export FLASK_APP=backend/__init__.py
   flask run --port 5000
   ```
   La app estará disponible en `http://localhost:5000`.

5. **Acceder al frontend**  
   Navega a `http://localhost:5000` y verás el tablero Kanban.

## Flujo de Datos Clave

1. **Carga inicial**  
   *El navegador hace una petición `GET /api/tasks`. El backend lee `tasks.json`, devuelve la lista, y el script añade tarjetas al DOM.*

2. **Creación de tarea**  
   *Formulario en la columna “Por Hacer” envía `POST /api/tasks` con `content`. Backend asigna un ID incremental, guarda el archivo y responde con la nueva tarea que se inserta en el tablero.*

3. **Actualización (editado o movido)**  
   *Al hacer clic en una tarjeta se muestra `prompt`; al confirmar, el cliente envía `PUT /api/tasks/<id>` con los cambios. El backend actualiza el JSON y devuelve la tarea modificada; el script mueve la tarjeta si el estado cambió.*

4. **Eliminación** *(no expuesta por UI)*  
   *Si se llamara a `DELETE /api/tasks/<id>`, el backend eliminaría la entrada del array y persistiría el cambio.*

## Extensiones Futuras (Opcional)

| Área | Posible mejora |
|------|----------------|
| **Autenticación** | Añadir JWT para proteger las rutas y asociar tareas a usuarios. |
| **Persistencia en BD** | Migrar de `tasks.json` a SQLite/PostgreSQL usando SQLAlchemy. |
| **WebSocket** | Implementar actualizaciones en tiempo real con Flask‑SocketIO para que varios clientes vean los cambios simultáneamente. |
| **Pruebas automatizadas** | Integrar pytest y Selenium para pruebas unitarias del backend y de integración end‑to‑end del frontend. |
| **UI/UX** | Añadir drag‑and‑drop más robusto con una librería como `SortableJS` y permitir la edición inline sin prompt. |

---