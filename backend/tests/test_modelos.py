from backend.modelos import Task

def test_task_creation():
    task = Task('1', 'Buy groceries', 'To Do')
    assert task.id == '1'
    assert task.content == 'Buy groceries'
    assert task.state == 'To Do'