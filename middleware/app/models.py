from sqlmodel import SQLModel, Field, Column, Integer, String, ARRAY
from typing import Optional
from pydantic import BaseModel
from app.database import Base

class Audit(Base):
    __tablename__ = "audit"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    headers = Column("headers", ARRAY(String))
    method = Column(String)
    response = Column(String)

class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass

# item model
class Item(BaseModel):
    name: str

class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)