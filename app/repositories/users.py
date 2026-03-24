from typing import List, Optional
from bson import ObjectId
from ..schemas.users import UserCreate, UsersResponse
from .base import AbstractTaskRepository
from ..database.database import database


class MongoUserRepository(AbstractTaskRepository):
    def __init__(self):
        self.collection = database.db["users"]

    def get_all(self) -> List[UsersResponse]:
        users = []
        for doc in self.collection.find():
            users.append(
                UsersResponse(
                    id=str(doc["_id"]),
                    name=doc["name"],
                    email=doc["email"],
                    idade=doc["idade"],
                )
            )
        return users

    def get_by_id(self, user_id: str) -> Optional[UsersResponse]:
        doc = self.collection.find_one({"_id": ObjectId(user_id)})

        if not doc:
            return None

        return UsersResponse(
            id=str(doc["_id"]),
            name=doc["name"],
            email=doc["email"],
            idade=doc["idade"],
        )

    def insert(self, user: UserCreate) -> UsersResponse:
        result = self.collection.insert_one(user.model_dump())

        return UsersResponse(
            id=str(result.inserted_id),
            name=user.name,
            email=user.email,
            idade=user.idade,
        )

    def update(self, user: UsersResponse) -> UsersResponse:
        self.collection.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": user.model_dump(exclude={"id"})}
        )
        return user

    def delete(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0