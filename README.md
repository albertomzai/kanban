# Visión General del Proyecto

Este proyecto es una aplicación web sencilla de un tablero Kanban implementada con Flask para el backend y HTML/JavaScript para el frontend. El objetivo principal es proporcionar una interfaz para gestionar tareas en diferentes estados: "Por Hacer", "En Progreso" y "Hecho". La aplicación permite crear, leer, actualizar y eliminar tareas (CRUD) a través de una API RESTful.

El backend utiliza Flask como framework web y gestiona las solicitudes HTTP. Las tareas se almacenan en un archivo JSON (`tasks.json`) para mantener la simplicidad del proyecto. El frontend es una página HTML que se sirve estáticamente y utiliza JavaScript para interactuar con la API del backend.

# Arquitectura del Sistema

El sistema consta de dos partes principales: el backend y el frontend.

## Backend

| **Componente** | **Descripción** |
|----------------|-----------------|
| `app.py`       | Punto de entrada principal que crea y ejecuta la aplicación Flask. |
| `requirements.txt` | Archivo de requisitos para instalar las dependencias necesarias (Flask, pytest). |
| `backend/__init__.py` | Configura la aplicación Flask y registra el Blueprint de rutas (`api_bp`). También define una ruta raíz que sirve el archivo `index.html` del frontend. |
| `backend/routes.py` | Define los endpoints de la API para gestionar las tareas (CRUD). Las tareas se almacenan en un archivo JSON (`tasks.json`). |

## Frontend

| **Componente** | **Descripción** |
|----------------|-----------------|
| `frontend/index.html` | Página HTML que muestra el tablero Kanban. Utiliza Bootstrap para el estilo y JavaScript para interactuar con la API del backend. |

# Endpoints de la API

La API proporciona los siguientes endpoints:

| **Endpoint**   | **Método HTTP** | **Descripción** |
|----------------|-----------------|-----------------|
| `/api/tasks`     | GET             | Obtiene todas las tareas. |
| `/api/tasks`     | POST            | Crea una nueva tarea. Se requiere un objeto JSON con la propiedad `content`. |
| `/api/tasks/<task_id>` | PUT           | Actualiza una tarea existente. Se puede actualizar el contenido (`content`) o el estado (`state`). |
| `/api/tasks/<task_id>` | DELETE        | Elimina una tarea existente. |

# Instrucciones de Instalación y Ejecución

1. Clona el repositorio del proyecto.
2. Navega al directorio raíz del proyecto.
3. Crea un entorno virtual e instala las dependencias:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```sh
   python app.py
   ```
5. Abre tu navegador y ve a `http://127.0.0.1:5000/` para ver el tablero Kanban.

# Flujo de Datos Clave

El flujo de datos principal del sistema es el siguiente:

1. **Solicitud HTTP**: El usuario interactúa con la interfaz web frontend, que envía solicitudes HTTP a la API backend.
2. **Procesamiento Backend**: La API backend procesa las solicitudes y manipula los datos almacenados en `tasks.json`.
3. **Actualización de Datos**: Los cambios en los datos se reflejan en el archivo JSON y se devuelven al frontend.
4. **Actualización Frontend**: El frontend actualiza la interfaz en función de la respuesta de la API.

# Extensiones Futuras

Aunque el proyecto proporciona una funcionalidad básica, hay varias extensiones que podrían mejorarlo:

1. **Base de Datos**: Cambiar el almacenamiento de tareas de un archivo JSON a una base de datos como SQLite o PostgreSQL para mayor escalabilidad y rendimiento.
2. **Autenticación**: Implementar autenticación y autorización para permitir que diferentes usuarios gestionen sus propias listas de tareas.
3. **Notificaciones**: Agregar notificaciones push para alertar a los usuarios sobre actualizaciones en sus tareas.
4. **Historial de Cambios**: Registrar un historial de cambios para cada tarea para rastrear su evolución a lo largo del tiempo.
5. **Interfaz de Usuario Mejorada**: Mejorar la interfaz frontend con más características y una mejor experiencia de usuario.

Estas extensiones podrían ser consideradas en futuras iteraciones del proyecto, dependiendo de las necesidades y los objetivos específicos del equipo.