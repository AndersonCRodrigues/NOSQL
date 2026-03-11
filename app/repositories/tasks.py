from typing import List, Optional
from bson import ObjectId
from ..schemas.tasks import TaskResponse, TaskCreate
from .base import AbstractTaskRepository
from ..database.database import database


class MongoTaskRepository(AbstractTaskRepository):
    def __init__(self):
        self.collection = database.db["tasks"]

    def get_all(self) -> List[TaskResponse]:
        tasks = []
        for doc in self.collection.find():
            tasks.append(
                TaskResponse(
                    id=str(doc["_id"]),
                    title=doc["title"],
                    completed=doc["completed"]
                )
            )
        return tasks

    def get_by_id(self, task_id: str) -> Optional[TaskResponse]:
        doc = self.collection.find_one({"_id": ObjectId(task_id)})

        if not doc:
            return None

        return TaskResponse(
            id=str(doc["_id"]),
            title=doc["title"],
            completed=doc["completed"]
        )

    def insert(self, task: TaskCreate) -> TaskResponse:
        result = self.collection.insert_one(task.model_dump())

        return TaskResponse(
            id=str(result.inserted_id),
            title=task.title,
            completed=task.completed
        )

    def update(self, task: TaskResponse) -> TaskResponse:
        self.collection.update_one(
            {"_id": ObjectId(task.id)},
            {"$set": task.model_dump(exclude={"id"})}
        )
        return task

    def delete(self, task_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0