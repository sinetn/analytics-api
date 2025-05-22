from typing import List, Optional
from pydantic import BaseModel, Field

'''
id
path
description
'''


class EventCreateSchema(BaseModel):
    page: str
    description: Optional[str] = Field(
        default="The description of the event")  # optional field


class EventUpdateSchema(BaseModel):
    description: str


class EventSchema(BaseModel):
    id: int  # required field
    page: Optional[str] = ""  # optional field
    description: Optional[str] = ""  # optional field


class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int
