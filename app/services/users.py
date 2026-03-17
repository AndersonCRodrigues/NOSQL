from typing import List, Optional

from ..repositories.base import AbstractTaskRepository
from ..schemas.users import UsersResponse, UserCreate, UsersUpdate


class UsersService:

    def __init__(self, repo: AbstractTaskRepository):
        self.repo = repo

    def get_all(self) -> List[UsersResponse]:
        return self.repo.get_all()

    def get_by_id(self, user_id: str) -> Optional[UsersResponse]:
        return self.repo.get_by_id(user_id)

    def create(self, data: UserCreate) -> UsersResponse:
        return self.repo.insert(data)

    def update(self, user_id: str, data: UsersUpdate) -> Optional[UsersResponse]:
        user = self.repo.get_by_id(user_id)
        if user is None:
            return None
        updated = user.model_copy(update=data.model_dump(exclude_none=True))
        return self.repo.update(updated)

    def delete(self, user_id: str) -> bool:
        return self.repo.delete(user_id)
