from typing import List, Optional
from datetime import datetime, timezone
# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field
import sqlmodel
'''
id
path
description
'''


def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    # id: int  # required field
    page: Optional[str] = ""  # optional field
    description: Optional[str] = ""  # optional field
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")  # optional field


class EventUpdateSchema(SQLModel):
    description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int
