# Kanban Backend API

This repository contains the backend implementation for a simple Kanban board application.

## API Endpoints

### GET /api/tasks
- Returns all tasks in JSON format.

### POST /api/tasks
- Creates a new task. Expects JSON body:

```json
{
  "content": "Task description",
  "status": "Por Hacer"   // optional, defaults to 'Por Hacer'
}```

### PUT /api/tasks/<id>
- Updates an existing task. Body may contain `content` and/or `status`.

### DELETE /api/tasks/<id>
- Deletes the specified task.

## Running the Server

```bash
pip install -r requirements.txt
python app.py
```
