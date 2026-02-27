import uuid
from typing import List, Optional

from ..repositories.base import AbstractTaskRepository
from ..schemas.tasks import TaskCreate, TaskResponse, TaskUpdate


class TaskService:

    def __init__(self, repo: AbstractTaskRepository):
        self.repo = repo

    def get_all(self) -> List[TaskResponse]:
        return self.repo.get_all()

    def get_by_id(self, task_id: str) -> Optional[TaskResponse]:
        return self.repo.get_by_id(task_id)

    def create(self, data: TaskCreate) -> TaskResponse:
        task = TaskResponse(
            id=str(uuid.uuid4()),
            title=data.title,
            completed=data.completed,
        )
        return self.repo.insert(task)

    def update(self, task_id: str, data: TaskUpdate) -> Optional[TaskResponse]:
        task = self.repo.get_by_id(task_id)
        if task is None:
            return None
        updated = task.model_copy(update=data.model_dump(exclude_none=True))
        return self.repo.update(updated)

    def delete(self, task_id: str) -> bool:
        return self.repo.delete(task_id)
