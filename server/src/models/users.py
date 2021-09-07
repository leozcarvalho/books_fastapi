from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.models.books import *
from src.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    books = relationship("Books", backref="users", cascade="all, delete")