from .config import settings
from pymongo import MongoClient

class MongoDB:
    def __init__(self, url: str = settings.DATABASE_URL):
        self.client = MongoClient(url)
        self.db = self.client["my_db"]

database = MongoDB()
