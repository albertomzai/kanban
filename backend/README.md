# Backend API – Kanban Board

## Endpoints

- **GET /api/tasks**: Retrieve all tasks.

- **POST /api/tasks**: Create a new task. Body must contain `content` (string) and optionally `status`. Status defaults to "Por Hacer" if omitted.

- **PUT /api/tasks/&lt;id&gt;**: Update an existing task. Body may include `content` and/or `status`.

- **DELETE /api/tasks/&lt;id&gt;**: Delete a task by its ID.

## Data Persistence

Tasks are stored in `tasks.json` at the project root. The file is accessed with a thread‑safe lock to prevent concurrent write issues.

## Running the Server

```bash
python app.py
```
The server listens on port 5000 and serves the frontend from the `frontend/` directory.

## Testing

Run the test suite with:

`pytest`