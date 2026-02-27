from typing import Dict, List, Optional

from ..schemas.tasks import TaskResponse


_tasks: Dict[str, TaskResponse] = {}


def get_all() -> List[TaskResponse]:
    return list(_tasks.values())


def get_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def insert(task: TaskResponse) -> TaskResponse:
    _tasks[task.id] = task
    return task


def update(task: TaskResponse) -> TaskResponse:
    _tasks[task.id] = task
    return task


def delete(task_id: str) -> bool:
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False
