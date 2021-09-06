from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    read: bool

class Book(BookBase):
    id: int

    class Config:
	    orm_mode=True

class BookComplete(BookBase):
    owner_id: int

    class Config:
	    orm_mode=True

class Status(BaseModel):
    message: str



