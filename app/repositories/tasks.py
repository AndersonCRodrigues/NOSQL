from typing import List, Optional
from bson import ObjectId
from ..schemas.tasks import TaskResponse, TaskCreate
from .base import AbstractTaskRepository
from ..database.database import databaseAsync as database


class MongoTaskRepository(AbstractTaskRepository):
    def __init__(self):
        # Certifique-se que database.db vem de um AsyncIOMotorClient
        self.collection = database.db["tasks"]

    async def get_all(self) -> List[TaskResponse]:
        tasks = []
        # No Motor, find() retorna um cursor assíncrono
        async for doc in self.collection.find():
            tasks.append(
                TaskResponse(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    completed=doc["completed"]
                )
            )
        return tasks

    async def get_by_id(self, task_id: str) -> Optional[TaskResponse]:
        # find_one precisa de await
        doc = await self.collection.find_one({"_id": ObjectId(task_id)})

        if not doc:
            return None

        return TaskResponse(
            id=str(doc["_id"]),
            title=doc["title"],
            completed=doc["completed"]
        )

    async def insert(self, task: TaskCreate) -> TaskResponse:
        result = await self.collection.insert_one(task.model_dump())

        return TaskResponse(
            id=str(result.inserted_id),
            title=task.title,
            completed=task.completed
        )

    async def update(self, task: TaskResponse) -> TaskResponse:
        # Precisa de await
        await self.collection.update_one(
            {"_id": ObjectId(task.id)},
            {"$set": task.model_dump(exclude={"id"})}
        )
        return task

    async def delete(self, task_id: str) -> bool:
        # Precisa de await
        result = await self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0