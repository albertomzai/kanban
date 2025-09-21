# Visión General del Proyecto

Este proyecto es una aplicación web simple que permite gestionar tareas. La aplicación utiliza Flask como framework de back-end y almacena las tareas en un archivo JSON llamado `tasks.json`. Los usuarios pueden realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre las tareas a través de una API RESTful.

La aplicación se compone principalmente de dos partes: el back-end, desarrollado con Flask y Python, y el front-end, que interactúa con la API para mostrar y manipular las tareas. El front-end no está incluido en el contexto proporcionado, pero asumimos que existe un archivo `index.html` en la carpeta `frontend`.

El flujo de datos principal comienza cuando el usuario accede a la aplicación web. La aplicación carga la página principal desde el archivo `index.html`. A partir de ahí, el front-end interactúa con la API del back-end para obtener, crear, actualizar y eliminar tareas.

# Arquitectura del Sistema

La arquitectura del sistema se basa en una estructura simple de Flask con un blueprint para las rutas de la API. La aplicación está organizada en dos archivos principales: `__init__.py` y `routes.py`.

## Estructura de Archivos
- **__init__.py**: Este archivo contiene la configuración principal de la aplicación Flask, incluyendo el registro del blueprint `api_bp`.
- **routes.py**: Este archivo define las rutas de la API y las operaciones CRUD sobre las tareas.

## Diagrama de Componentes

```mermaid
graph TD
    A[Frontend] --> B[Flask App]
    B --> C[Blueprint: api_bp]
    C --> D[TASKS_FILE (tasks.json)]
```

## Endpoints de la API

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| /tasks   | GET    | Obtiene todas las tareas. |
| /tasks   | POST   | Crea una nueva tarea. |
| /tasks/<int:task_id> | PUT  | Actualiza una tarea existente por su ID. |
| /tasks/<int:task_id> | DELETE | Elimina una tarea existente por su ID. |

# Instrucciones de Instalación y Ejecución

1. **Clona el repositorio del proyecto**:
    ```bash
    git clone <URL_REPOSITORIO>
    cd nombre_del_proyecto
    ```

2. **Crea un entorno virtual y activa**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows use `venv\Scripts\activate`
    ```

3. **Instala las dependencias**:
    ```bash
    pip install flask
    ```

4. **Ejecuta la aplicación**:
    ```bash
    python app.py
    ```

5. **Accede a la aplicación en el navegador**:
    Abre tu navegador y ve a `http://localhost:5000`.

# Flujo de Datos Clave

1. **Inicio de la Aplicación**: El usuario accede a la URL principal de la aplicación (`/`).
2. **Carga del Frontend**: La aplicación carga el archivo `index.html` desde la carpeta `frontend`.
3. **Interacción con la API**:
    - **Obtener Tareas**: El front-end realiza una solicitud GET a `/tasks` para obtener todas las tareas.
    - **Crear Tarea**: El front-end envía una solicitud POST a `/tasks` con los datos de la nueva tarea.
    - **Actualizar Tarea**: El front-end envía una solicitud PUT a `/tasks/<task_id>` con los datos actualizados de la tarea.
    - **Eliminar Tarea**: El front-end envía una solicitud DELETE a `/tasks/<task_id>` para eliminar la tarea.

4. **Manejo de Datos**:
    - Las solicitudes GET y POST interactúan con el archivo `tasks.json` para leer y escribir tareas, respectivamente.
    - Las solicitudes PUT y DELETE actualizan o eliminan tareas en el archivo `tasks.json`.

# Extensiones Futuras

1. **Base de Datos**: Migrar la persistencia de datos desde un archivo JSON a una base de datos relacional como PostgreSQL o MySQL para mejorar la escalabilidad y rendimiento.
2. **Autenticación y Autorización**: Implementar un sistema de autenticación (por ejemplo, JWT) para permitir que los usuarios se registren e inicien sesión, y gestionar sus tareas de manera personalizada.
3. **Validaciones Adicionales**: Añadir más validaciones a los datos recibidos en las solicitudes POST y PUT para garantizar la integridad de los datos.
4. **Documentación de la API**: Generar documentación automática para la API utilizando herramientas como Swagger o OpenAPI para facilitar el uso y desarrollo por parte de otros desarrolladores.
5. **Pruebas Unitarias**: Implementar pruebas unitarias para las rutas de la API para asegurar que funcionen correctamente en diferentes escenarios.

Este documento proporciona una visión completa y detallada del proyecto, incluyendo su arquitectura, endpoints de la API, instrucciones de instalación y ejecución, flujo de datos clave y sugerencias para extensiones futuras.