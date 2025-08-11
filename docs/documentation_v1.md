We need markdown doc. Include sections. Use mermaid diagram for architecture: Flask app with routes, tasks_manager module, static SPA. Provide endpoints list. Installation instructions pip install -r requirements.txt run backend.py. Flow of data: create->save->read etc. Let's craft.# Documentación Técnica del Proyecto Kanban Mini‑Trello

## Visión General del Proyecto
Kanban Mini‑Trello es una aplicación ligera que permite gestionar tareas en un tablero Kanban con tres columnas: **Por Hacer**, **En Progreso** y **Hecho**.  
- **Back‑end**: Flask (Python 3) expone una API REST para CRUD de tareas y sirve la SPA desde el directorio `static`.  
- **Front‑end**: Una única página HTML (`index.html`) con JavaScript puro que consume la API, renderiza las tarjetas y permite arrastrar/soltar entre columnas.  
- **Persistencia**: Los datos se guardan en un archivo JSON (`tasks.json`).  

El proyecto incluye pruebas unitarias con `pytest` y una configuración mínima de dependencias (`requirements.txt`).

---

## Arquitectura del Sistema

```mermaid
graph TD
    A[Cliente Web] -->|HTTP/JSON| B[Flask App]
    B --> C[Endpoint /api/tasks (GET, POST)]
    B --> D[Endpoint /api/tasks/<id> (PUT, DELETE)]
    B --> E[Static Files (index.html, JS, CSS)]
    C & D --> F[tasks_manager.py] 
    F --> G[File System: tasks.json]
```

### Descripción de los componentes

| Componente | Responsabilidad |
|------------|-----------------|
| **Flask App (`backend.py`)** | Maneja las rutas API, valida datos y delega en `tasks_manager`. También sirve la SPA. |
| **`tasks_manager.py`** | Funciones puras para cargar, guardar, generar IDs y manipular tareas. Facilita pruebas unitarias. |
| **SPA (`static/index.html`)** | Interfaz de usuario: renderizado de tarjetas, drag‑and‑drop, edición inline y llamadas AJAX a la API. |
| **Persistencia (`tasks.json`)** | Almacena el estado actual del tablero en disco. |

---

## Endpoints de la API

| Método | Ruta | Descripción | Parámetros de Entrada | Respuesta (ejemplo) |
|--------|------|-------------|-----------------------|---------------------|
| `GET` | `/api/tasks` | Lista todas las tareas. | Ninguno | `{ "tasks": [ { "id": 1, "content": "...", "state": "Por Hacer" }, … ] }` |
| `POST` | `/api/tasks` | Crea una nueva tarea. | `{"content":"texto","state":"Por Hacer"}` | `201 Created`: `{ "id": 2, "content":"texto", "state":"Por Hacer" }` |
| `PUT` | `/api/tasks/<int:id>` | Actualiza contenido y/o estado de una tarea existente. | `{"content":"nuevo","state":"En Progreso"}` | `200 OK`: `{ "id": 2, "content":"nuevo", "state":"En Progreso" }` |
| `DELETE` | `/api/tasks/<int:id>` | Elimina la tarea con el ID especificado. | Ninguno | `200 OK`: `{ "message": "Task deleted successfully." }` |

> **Nota**: Todos los endpoints aceptan y devuelven JSON; se aplica CORS para permitir llamadas desde el mismo dominio.

---

## Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio (o copiar los archivos)**  
   ```bash
   git clone <url_del_repositorio>
   cd kanban-mini-trello
   ```

2. **Crear un entorno virtual** *(opcional pero recomendado)*  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar el archivo de tareas (solo la primera ejecución)**  
   El script `backend.py` crea automáticamente `tasks.json` si no existe.

5. **Ejecutar el servidor Flask**  
   ```bash
   python backend.py
   ```
   Por defecto, el servidor escucha en `http://0.0.0.0:5000/`.

6. **Acceder a la aplicación**  
   Abrir un navegador y navegar a `http://localhost:5000/`. La SPA se cargará automáticamente.

7. **Ejecutar pruebas unitarias** *(opcional)*  
   ```bash
   pytest tests/test_backend.py
   ```

---

## Flujo de Datos Clave

1. **Creación de una tarea**
   - El usuario escribe texto y pulsa “Añadir”.
   - JavaScript envía `POST /api/tasks` con JSON `{content, state:"Por Hacer"}`.
   - Flask valida el contenido y estado → genera ID → llama a `tasks_manager.save_tasks`.
   - Respuesta contiene la tarea creada; JS añade una tarjeta al DOM.

2. **Actualización de estado (drag‑and‑drop)**
   - Al soltar una tarjeta en otra columna, JS captura el nuevo estado.
   - Envía `PUT /api/tasks/<id>` con `{state: nuevoEstado}`.
   - Flask actualiza la tarea y persiste → respuesta vacía; JS mueve la tarjeta.

3. **Edición inline de contenido**
   - Doble clic convierte la tarjeta en un `<input>`.
   - Al perder foco o pulsar Enter, se envía `PUT /api/tasks/<id>` con `{content: nuevoTexto}`.
   - Flask actualiza y persiste; JS reemplaza el input por la tarjeta actualizada.

4. **Eliminación de una tarea**
   - Se dispara desde un botón (no incluido en el código base pero previsto por el plan).
   - JS envía `DELETE /api/tasks/<id>`.
   - Flask elimina la entrada y responde con mensaje; JS remueve la tarjeta del DOM.

5. **Carga inicial del tablero**
   - Al cargar la página, JS hace `GET /api/tasks` para poblar las columnas.
   - La respuesta se procesa en `renderTasks`, que construye tarjetas y las inserta en sus columnas correspondientes.

---

## Extensiones Futuras (de acuerdo al plan de construcción)

- **Botón de eliminación**: Añadir un icono “X” a cada tarjeta que invoque el endpoint DELETE.  
- **Persistencia más robusta**: Migrar a una base de datos SQLite o PostgreSQL para concurrencia y escalabilidad.  
- **Autenticación**: JWT o sesiones para usuarios multi‑usuario.  
- **Test de integración front‑end**: Utilizar Cypress o Playwright.

---

### Contacto
Para dudas, mejoras o contribuciones, abre un issue en el repositorio GitHub correspondiente.