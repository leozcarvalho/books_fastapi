from pydantic import BaseModel
from typing import List, Optional

from src.schemas.books import *

class UserBase(BaseModel):
    name: str
    email: str

    class Config:
	    orm_mode=True

class User(UserBase):
    id: int

class UserComplete(User):
    books: Optional[List[Book]] = None


class Status(BaseModel):
    message: str


class AllUsers(BaseModel):
    users_total_count: int
    users: List[User]
    
    class Config:
        orm_mode=True

