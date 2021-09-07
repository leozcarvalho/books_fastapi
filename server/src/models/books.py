from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.schema import ForeignKey
from src.models.users import *
from sqlalchemy.orm import relationship
from src.database.database import Base

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(255), index=True, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    owner_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    