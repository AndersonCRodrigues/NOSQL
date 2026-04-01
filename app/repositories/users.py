from pymongo import ASCENDING
from typing import List, Optional
from bson import ObjectId
from ..schemas.users import UserCreate, UsersResponse
from .base import AbstractTaskRepository # Note: Talvez queira renomear para AbstractUserRepository?
from ..database.database import databaseAsync as database

class MongoUserRepository(AbstractTaskRepository):
    def __init__(self):
        self.collection = database.db["users"]

    async def create_indexes(self):
        await self.collection.create_index(
            [("email", ASCENDING)],
            unique=True
        )

    async def get_all(self) -> List[UsersResponse]:
        users = []
        async for doc in self.collection.find():
            users.append(
                UsersResponse(
                    id=str(doc["_id"]),
                    name=doc["name"],
                    email=doc["email"],
                    idade=doc["idade"],
                )
            )
        return users

    async def get_by_id(self, user_id: str) -> Optional[UsersResponse]:
        doc = await self.collection.find_one({"_id": ObjectId(user_id)})

        if not doc:
            return None

        return UsersResponse(
            id=str(doc["_id"]),
            name=doc["name"],
            email=doc["email"],
            idade=doc["idade"],
        )

    async def insert(self, user: UserCreate) -> UsersResponse:
        # await necessário e inserted_id funciona igual ao PyMongo
        result = await self.collection.insert_one(user.model_dump())

        return UsersResponse(
            id=str(result.inserted_id),
            name=user.name,
            email=user.email,
            idade=user.idade,
        )

    async def update(self, user: UsersResponse) -> UsersResponse:
        await self.collection.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": user.model_dump(exclude={"id"})}
        )
        return user

    async def delete(self, user_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0