from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    idade: int


class UsersUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    idade: Optional[int] = None
   


class UsersResponse(BaseModel):
    id: str
    name: str
    email: str
    idade: int