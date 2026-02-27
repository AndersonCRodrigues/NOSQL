from typing import Dict, List, Optional

from ..schemas.tasks import TaskResponse
from .base import AbstractTaskRepository

_tasks: Dict[str, TaskResponse] = {}


class MemoryTaskRepository(AbstractTaskRepository):

    def get_all(self) -> List[TaskResponse]:
        return list(_tasks.values())

    def get_by_id(self, task_id: str) -> Optional[TaskResponse]:
        return _tasks.get(task_id)

    def insert(self, task: TaskResponse) -> TaskResponse:
        _tasks[task.id] = task
        return task

    def update(self, task: TaskResponse) -> TaskResponse:
        _tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        if task_id in _tasks:
            del _tasks[task_id]
            return True
        return False
