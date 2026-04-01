from ..config import settings
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    def __init__(self, url: str = settings.DATABASE_URL):
        self.client = MongoClient(url)
        self.db = self.client["my_db"]

class MongoMotorDB:
    def __init__(self, url: str = settings.DATABASE_URL) -> None:
        self.client = AsyncIOMotorClient(url)
        self.db = self.client["my_db"]

databaseAsync = MongoMotorDB()
database = MongoDB()
