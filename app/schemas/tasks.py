from pydantic import BaseModel

class TaskModel(BaseModel):
    id: str = None
    title:str = None
    completed: bool = False
    
    