# Visión General del Proyecto

Kanban Mini‑Trello es una aplicación web sencilla que permite gestionar tareas en un tablero Kanban con tres columnas: **Por Hacer**, **En Progreso** y **Hecho**.  
El backend está construido sobre Flask y expone una API RESTful para crear, leer, actualizar y eliminar tareas persistidas en un archivo JSON local (`tasks.json`). El frontend es una única página HTML que consume la API mediante `fetch` y ofrece interactividad con Bootstrap 5 y drag‑and‑drop nativo del navegador.

## Flujo de Datos Clave

1. **Carga inicial**  
   - Al abrir el sitio, el script `loadTasks()` hace un GET a `/api/tasks`.  
   - La respuesta (lista de objetos `{id, content, state}`) se renderiza en las columnas correspondientes.

2. **Creación de tarea**  
   - El formulario “Nueva tarea” envía un POST a `/api/tasks` con el campo `content`.  
   - El servidor asigna un ID incremental y devuelve la nueva tarea; el cliente la añade al DOM.

3. **Edición**  
   - Al hacer doble clic en el contenido de una tarjeta, se reemplaza por un input editable.  
   - Cuando el input pierde foco o se pulsa Enter, se envía un PUT a `/api/tasks/<id>` con `content`.  
   - El servidor actualiza la tarea y devuelve la versión modificada; el cliente actualiza el texto.

4. **Cambio de estado (drag‑and‑drop)**  
   - Al soltar una tarjeta en otra columna, el cliente envía un PUT a `/api/tasks/<id>` con `state` igual al nombre de la columna objetivo.  
   - El servidor persiste el cambio y el cliente mueve la tarjeta dentro del DOM.

5. **Eliminación**  
   - Al pulsar el botón “×” en una tarjeta, se envía un DELETE a `/api/tasks/<id>`.  
   - Si la respuesta es 200, el cliente elimina la tarjeta del DOM.

---

# Arquitectura del Sistema

## Componentes principales

| Componente | Tecnologías | Responsabilidad |
|------------|-------------|-----------------|
| **Flask** | Python, Flask | Servidor web que expone la API REST y sirve los archivos estáticos. |
| **API Blueprint (`backend.routes`)** | Flask Blueprint | Rutas `/api/tasks` con métodos GET, POST, PUT, DELETE. |
| **Persistencia** | Archivo JSON (`tasks.json`) | Almacena el estado de las tareas entre reinicios del servidor. |
| **Frontend** | HTML5, CSS3 (Bootstrap 5), JavaScript | Interfaz de usuario Kanban con drag‑and‑drop y consumo de la API. |

## Diagrama de flujo

```mermaid
flowchart TD
    A[Usuario] --> B[Browser]
    B --> C{JavaScript}
    C --> D[fetch /api/tasks (GET)]
    D --> E[Flask App]
    E --> F[backend.routes.get_tasks]
    F --> G[Read tasks.json]
    G --> H[Return JSON]
    H --> C
    C --> I[Render tareas en columnas]

    subgraph CRUD
        J[Crear tarea] --> K[POST /api/tasks]
        L[Actualizar] --> M[PUT /api/tasks/<id>]
        N[Eliminar] --> O[DELETE /api/tasks/<id>]
    end

    style CRUD fill:#f9f,stroke:#333,stroke-width:2px
```

---

# Endpoints de la API

| Método | Ruta | Parámetros | Cuerpo | Respuesta | Código |
|--------|------|------------|--------|-----------|--------|
| **GET** | `/api/tasks` | N/A | N/A | Lista JSON de tareas | 200 |
| **POST** | `/api/tasks` | `content` (string) | `{ "content": "..."} ` | Tarea creada con ID y estado inicial | 201 |
| **PUT** | `/api/tasks/<int:task_id>` | `content` (opcional), `state` (opcional) | `{ "content": "...", "state": "..." }` | Tarea actualizada | 200 |
| **DELETE** | `/api/tasks/<int:task_id>` | N/A | N/A | Mensaje de éxito | 200 |

### Ejemplo de llamada

```bash
curl -X POST http://localhost:5000/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"content":"Revisar PR"}'
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone <url_del_repositorio>
   cd <nombre_del_proyecto>
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**  
   ```bash
   python app.py
   ```
   La API estará disponible en `http://0.0.0.0:5000` y el frontend se servirá desde `/`.

5. **Pruebas unitarias**  
   ```bash
   pytest tests/test_backend.py
   ```

---

# Extensiones Futuras

| Área | Posible mejora |
|------|----------------|
| **Persistencia** | Migrar a una base de datos SQLite o PostgreSQL para concurrencia y rendimiento. |
| **Autenticación** | Añadir JWT o OAuth2 para proteger la API y permitir usuarios con tareas propias. |
| **WebSocket** | Implementar actualizaciones en tiempo real usando Flask‑SocketIO, evitando recargas manuales. |
| **UI/UX** | Integrar drag‑and‑drop más robusto (Dragula, SortableJS) y permitir edición inline de estado con selectores. |
| **Testing** | Añadir pruebas de integración end‑to‑end con Selenium o Cypress para el frontend. |

---