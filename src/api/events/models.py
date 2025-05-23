from typing import List, Optional
# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field
'''
id
path
description
'''


class EventModel(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    # id: int  # required field
    page: Optional[str] = ""  # optional field
    description: Optional[str] = ""  # optional field


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")  # optional field


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int
