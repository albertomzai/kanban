<think>
Okay, I need to act as both a software architecture expert and a technical writer to create a comprehensive Markdown documentation based solely on the provided code context. The user wants me to strictly follow their section guidelines for style and structure.

First, let's analyze all the files to understand what this project is about. From the filenames and code snippets:

1. The main backend app uses Flask with routes defined in `routes.py`
2. There's a task model in `modelos.py` with an id, content, and state
3. Data storage uses JSON file operations via `repositorio.py`
4. Frontend is built with Bootstrap and has drag-and-drop Kanban board functionality
5. There are test files for both models and repository

This appears to be a simple task management system with three Kanban columns: To-Do, In Progress, Done. The frontend allows adding tasks and dragging them between columns (which triggers API updates). The backend stores tasks in tasks.json.

I need to follow their exact section order:
1. Vision General (narrative)
2. System Architecture & API Endpoints (technical with tables/diagrams)
3. Installation instructions
4. Key Data Flows
5. Future Extensions (optional)

Starting with the title as instructed - no other words before it.
</think>

# Kanban Task Manager: Technical Documentation