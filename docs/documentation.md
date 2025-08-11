Need produce markdown.# Visión General del Proyecto

Este proyecto es una **aplicación Kanban minimalista** que combina un backend RESTful en Flask con un frontend SPA (Single Page Application) puro en HTML/JavaScript. La aplicación permite crear, leer, actualizar y eliminar tareas distribuidas en tres columnas: *Por Hacer*, *En Progreso* y *Hecho*.  

- **Backend (`backend.py`)** expone cuatro endpoints CRUD sobre `/api/tasks` y sirve la SPA desde el directorio `static`.  
- **Persistencia**: los datos se guardan en un archivo JSON (`tasks.json`) a través del módulo de utilidades `tasks_manager.py`.  
- **Frontend (`index.html`)** consume la API con `fetch`, renderiza tarjetas (cards) y permite arrastrar‑soltar entre columnas, editar contenido al doble‑clic y eliminar tareas mediante drag‑and‑drop.  

El proyecto está pensado para ser ejecutado localmente, sin dependencias externas más allá de Flask, Flask‑Cors y pytest para pruebas.

---

# Arquitectura del Sistema

| Componente | Responsabilidad | Tecnologías |
|------------|-----------------|-------------|
| **Flask App** (`backend.py`) | Servidor web que expone la API REST y sirve el SPA. | Flask 3.x, Flask‑Cors |
| **API Endpoints** | Operaciones CRUD sobre tareas. | HTTP/JSON |
| **Persistencia** (`tasks.json`) | Almacén simple de tareas en disco. | JSON |
| **Módulo de utilidades** (`tasks_manager.py`) | Carga, guarda y manipula la lista de tareas. | Python estándar |
| **Frontend SPA** (`static/index.html`) | Interfaz gráfica: columnas Kanban, tarjetas, drag‑and‑drop. | HTML5, CSS3, Vanilla JS |

## Diagrama Mermaid

```mermaid
graph TD
    A[Usuario] --> B[Browser]
    B --> C[Flask App (backend.py)]
    C --> D[API Endpoints (/api/tasks...)]
    D --> E[tasks.json]
    C --> F[static/index.html]
    F --> G[JavaScript]
```

---

# Endpoints de la API

| Método | Ruta | Descripción | Parámetros de Entrada | Respuesta Esperada |
|--------|------|-------------|-----------------------|--------------------|
| **GET** | `/api/tasks` | Lista todas las tareas. | Ninguno | `200 OK`<br>`{ "tasks": [ { "id": int, "content": str, "state": str }, ... ] }` |
| **POST** | `/api/tasks` | Crea una nueva tarea. | `{ "content": str, "state": str (opcional)` | `201 Created`<br>`{ "id": int, "content": str, "state": str }` |
| **PUT** | `/api/tasks/<int:task_id>` | Actualiza contenido y/o estado de una tarea existente. | `{ "content": str (opcional), "state": str (opcional) }` | `200 OK`<br>`{ "id": int, "content": str, "state": str }` |
| **DELETE** | `/api/tasks/<int:task_id>` | Elimina la tarea con el ID especificado. | Ninguno | `200 OK`<br>`{ "message": "Task deleted successfully." }` |

### Detalle de Validaciones

- Los estados permitidos son `"Por Hacer"`, `"En Progreso"` y `"Hecho"`.  
- El campo `content` debe ser una cadena no vacía.  

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio** (o copiar los archivos).  
2. **Crear un entorno virtual** y activar:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar el servidor** (modo debug activado):

   ```bash
   python backend.py
   ```

5. Abrir un navegador y navegar a `http://localhost:5000`.  
6. Para ejecutar las pruebas unitarias:

   ```bash
   pytest tests/
   ```

---

# Flujo de Datos Clave

1. **Creación** (`POST /api/tasks`)  
   - El cliente envía JSON con `content` y opcionalmente `state`.  
   - Backend valida, genera un ID único (incremental), guarda en memoria y persiste a `tasks.json`.  
   - Responde con la tarea creada.

2. **Lectura** (`GET /api/tasks`)  
   - Backend carga el archivo JSON, devuelve la lista completa de tareas.

3. **Actualización** (`PUT /api/tasks/<id>`)  
   - Cliente envía cambios parciales (content y/o state).  
   - Backend localiza la tarea por ID, aplica los cambios, guarda y responde con la versión actualizada.

4. **Eliminación** (`DELETE /api/tasks/<id>`)  
   - Backend busca y elimina la entrada, persiste el archivo y devuelve un mensaje de éxito.

5. **Frontend**  
   - `fetchTasks()` carga todas las tareas al inicio y cada vez que se crea o actualiza una tarjeta.  
   - Drag‑and‑drop dispara `updateTask(id, { state: newState })`.  
   - Doble‑clic abre un input inline para editar el contenido.

---

# Extensiones Futuras

| Área | Posible Mejora |
|------|----------------|
| **Persistencia** | Migrar a una base de datos relacional (SQLite/PostgreSQL) o NoSQL (MongoDB) para escalabilidad y concurrencia. |
| **Autenticación** | Implementar JWT o sesiones para restringir el acceso a la API. |
| **Colaboración en tiempo real** | Añadir WebSocket (Flask‑SocketIO) para actualizar el tablero entre múltiples usuarios simultáneos. |
| **Pruebas de integración** | Automatizar pruebas end‑to‑end con Cypress o Playwright. |
| **CI/CD** | Configurar pipelines GitHub Actions que ejecuten tests y desplieguen a un entorno de staging. |

---