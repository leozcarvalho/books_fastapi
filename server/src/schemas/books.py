from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    read: bool

    class Config:
	    orm_mode=True

class Book(BookBase):
    id: int

class BookComplete(BookBase):
    owner_user: int

class Status(BaseModel):
    message: str



