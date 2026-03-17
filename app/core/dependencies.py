from fastapi import Depends

from ..repositories.base import AbstractTaskRepository
# from ..repositories.memory import MemoryTaskRepository
from ..repositories.tasks import MongoTaskRepository
from ..repositories.users import MongoUserRepository
from ..services.tasks import TaskService
from ..services.users import UsersService


def get_task_repository() -> AbstractTaskRepository:
    return MongoTaskRepository()

def get_task_service(
    repo: AbstractTaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repo)

def get_user_repository() -> AbstractTaskRepository:
    return MongoUserRepository()

def get_user_service(
    repo: AbstractTaskRepository = Depends(get_user_repository),
) -> TaskService:
    return UsersService(repo)