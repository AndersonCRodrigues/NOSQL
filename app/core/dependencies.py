from fastapi import Depends

from ..repositories.base import AbstractTaskRepository
from ..repositories.memory import MemoryTaskRepository
from ..services.tasks import TaskService


def get_task_repository() -> AbstractTaskRepository:
    return MemoryTaskRepository()


def get_task_service(
    repo: AbstractTaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repo)
