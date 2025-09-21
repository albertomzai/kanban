from backend.repositorio import TASKS_FILE, load_tasks, save_tasks

def test_load_tasks():
    tasks = [Task('1', 'Task 1', 'To Do')]
    with open(TASKS_FILE, 'w') as f:
        json.dump([t.__dict__ for t in tasks], f)

    loaded = load_tasks()
    assert len(loaded) == 1
    assert loaded[0]['id'] == '1'

def test_save_tasks():
    tasks = [Task('2', 'Task 2', 'In Progress')]
    save_tasks(tasks)

    with open(TASKS_FILE, 'r') as f:
        stored = json.load(f)

    assert len(stored) == 1
    assert stored[0]['id'] == '2'