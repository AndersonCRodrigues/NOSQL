from abc import ABC, abstractmethod
from typing import List, Optional

from ..schemas.tasks import TaskResponse


class AbstractTaskRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[TaskResponse]: ...

    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[TaskResponse]: ...

    @abstractmethod
    def insert(self, task: TaskResponse) -> TaskResponse: ...

    @abstractmethod
    def update(self, task: TaskResponse) -> TaskResponse: ...

    @abstractmethod
    def delete(self, task_id: str) -> bool: ...
