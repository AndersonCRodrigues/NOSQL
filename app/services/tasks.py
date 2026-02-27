import uuid
from typing import List, Optional

from ..schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from ..repositories import tasks as repo


def get_all() -> List[TaskResponse]:
    return repo.get_all()


def get_by_id(task_id: str) -> Optional[TaskResponse]:
    return repo.get_by_id(task_id)


def create(data: TaskCreate) -> TaskResponse:
    task = TaskResponse(
        id=str(uuid.uuid4()),
        title=data.title,
        completed=data.completed,
    )
    return repo.insert(task)


def update(task_id: str, data: TaskUpdate) -> Optional[TaskResponse]:
    task = repo.get_by_id(task_id)
    if task is None:
        return None

    updated = task.model_copy(update=data.model_dump(exclude_none=True))
    return repo.update(updated)


def delete(task_id: str) -> bool:
    return repo.delete(task_id)
