Need produce markdown.# Kanban Mini‑Trello – Documentación Técnica

---

## Visión General del Proyecto

Kanban Mini‑Trello es una aplicación web ligera que permite gestionar tareas en un tablero Kanban con tres columnas: **Por Hacer**, **En Progreso** y **Hecho**.  
El proyecto está dividido en dos partes:

1. **Backend (Flask)** – Expone una API RESTful para crear, leer, actualizar y eliminar tareas. La persistencia se realiza sobre un archivo JSON (`tasks.json`) mediante el módulo `tasks_manager`.  
2. **Frontend (SPA)** – Un único archivo HTML/JS que consume la API, renderiza las tarjetas en sus columnas correspondientes y permite arrastrar‑soltar para cambiar de estado.

El flujo de trabajo típico es:

- El usuario abre la página (`index.html`), el script hace una llamada `GET /api/tasks` y dibuja las tareas existentes.
- Al crear una nueva tarea con el botón “Añadir”, se envía un `POST /api/tasks`.  
- Cuando se arrastra una tarjeta a otra columna, se dispara un `PUT /api/tasks/<id>` para actualizar su estado.  
- El doble clic sobre la tarjeta abre un campo de edición y actualiza el contenido mediante otro `PUT`.  
- Se puede eliminar una tarea con un botón (no implementado en el frontend actualmente) que hace un `DELETE /api/tasks/<id>`.

---

## Arquitectura del Sistema

```mermaid
flowchart TD
    subgraph Frontend
        UI[<b>index.html</b><br/>SPA]
        API_CALLS["fetch('/api/...')"]
    end

    subgraph Backend
        FlaskApp[<b>Flask App (backend.py)</b>]
        TASKS_JSON[<b>tasks.json</b>]
        TasksManager["tasks_manager.py"]
    end

    UI -->|HTTP Requests| FlaskApp
    FlaskApp -->|Read/Write| TASKS_JSON
    FlaskApp -->|Helpers| TasksManager
```

### Componentes Clave

| Componente | Responsabilidad | Tecnologías |
|------------|-----------------|-------------|
| `backend.py` | Rutas API, validaciones de estado, manejo de errores. | Flask 3.x, Flask‑CORS |
| `tasks_manager.py` | Carga/guardado y operaciones CRUD sobre la lista de tareas. | Python estándar (`json`, `typing`) |
| `static/index.html` | SPA con lógica de UI (drag‑and‑drop, edición inline). | HTML5, CSS3, JavaScript ES6 |

---

## Endpoints de la API

| Método | Ruta | Parámetros | Cuerpo | Respuesta | Código HTTP |
|--------|------|------------|--------|-----------|-------------|
| `GET` | `/api/tasks` | ninguno | ninguno | `{ "tasks": [ {id, content, state}, ... ] }` | 200 |
| `POST` | `/api/tasks` | ninguno | `{ "content": str, "state": str (opcional) }` | Nueva tarea con ID generado | 201 |
| `PUT` | `/api/tasks/<int:task_id>` | `task_id` | `{ "content"?: str, "state"?: str }` | Tarea actualizada | 200 |
| `DELETE` | `/api/tasks/<int:task_id>` | `task_id` | ninguno | `{ "message": "Task deleted successfully." }` | 200 |

### Ejemplo de Uso

```bash
# Crear tarea
curl -X POST http://localhost:5000/api/tasks \
     -H 'Content-Type: application/json' \
     -d '{"content":"Revisar PR", "state":"Por Hacer"}'

# Obtener todas las tareas
curl http://localhost:5000/api/tasks

# Cambiar estado de una tarea
curl -X PUT http://localhost:5000/api/tasks/1 \
     -H 'Content-Type: application/json' \
     -d '{"state":"En Progreso"}'

# Eliminar tarea
curl -X DELETE http://localhost:5000/api/tasks/1
```

---

## Instrucciones de Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd kanban-mini-trello

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor Flask
export FLASK_APP=backend.py
flask run --host=0.0.0.0 --port=5000   # o simplemente: python backend.py

# 5. Acceder en navegador
open http://localhost:5000
```

### Pruebas Unitarias

```bash
pytest tests/test_backend.py
```

Las pruebas usan un archivo temporal para evitar modificar `tasks.json` real.

---

## Flujo de Datos Clave

1. **Carga Inicial**  
   - El frontend llama a `/api/tasks`.  
   - Flask lee `tasks.json`, devuelve la lista y el cliente la renderiza en las columnas correspondientes.

2. **Creación**  
   - Usuario escribe contenido y pulsa “Añadir”.  
   - Se envía `POST /api/tasks` con JSON `{content, state}`.  
   - Backend valida, genera un ID único (`generate_task_id`) y guarda el nuevo objeto en la lista.  
   - Devuelve el objeto creado; el frontend añade una tarjeta al DOM.

3. **Actualización**  
   - Arrastrar‑soltar o doble clic dispara `PUT /api/tasks/<id>`.  
   - Backend busca la tarea (`find_task_by_id`), actualiza los campos recibidos y persiste la lista.  
   - El cliente actualiza el estado visual de la tarjeta.

4. **Eliminación**  
   - Se envía `DELETE /api/tasks/<id>`.  
   - Backend elimina la entrada (`delete_task_by_id`) y devuelve un mensaje de éxito.  
   - El frontend debe remover la tarjeta del DOM (no implementado en el código actual).

---

## Extensiones Futuras

| Área | Posible Mejora | Justificación |
|------|----------------|---------------|
| **Persistencia** | Migrar a una base de datos relacional (SQLite/PostgreSQL) o NoSQL (MongoDB). | Escalabilidad, concurrencia y consultas más complejas. |
| **Autenticación** | Añadir JWT/Session para usuarios autenticados. | Permitir tableros privados por usuario. |
| **WebSocket** | Implementar comunicación en tiempo real con `Flask-SocketIO`. | Actualizaciones instantáneas entre clientes sin recargar la página. |
| **Frontend Framework** | Migrar a React/Vue/Angular. | Mejor manejo de estado, componentes reutilizables y pruebas unitarias del UI. |
| **Pruebas End‑to‑End** | Integrar Cypress o Playwright. | Validar flujos completos (creación → arrastre → eliminación). |
| **CI/CD** | Configurar GitHub Actions / GitLab CI para linting, tests y despliegue automático. | Garantizar calidad continua. |

---