from fastapi import Depends

from ..repositories.base import AbstractTaskRepository
# from ..repositories.memory import MemoryTaskRepository
from ..repositories.tasks import MongoTaskRepository
from ..services.tasks import TaskService


def get_task_repository() -> AbstractTaskRepository:
    return MongoTaskRepository()


def get_task_service(
    repo: AbstractTaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repo)
