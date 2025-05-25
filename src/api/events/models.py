from typing import List, Optional
from datetime import datetime, timezone
# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field
import sqlmodel
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now
'''
id
path
description
'''
# We are tracking page visits at any given time

# def get_utc_now(): # You can use the same function from timescaledb so I commented this one out
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class EventModel(TimescaleModel, table=True):
    page: str = Field(index=True)  # /about, /contact, /pages, /pricing
    # browser, os, device, etc.
    user_agent: Optional[str] = Field(default="", index=True)
    ip_address: Optional[str] = Field(
        default="", index=True)  # ip address of the user
    # referrer of the user like from google, facebook, etc. or its own website
    referrer: Optional[str] = Field(default="", index=True)
    session_id: Optional[str] = Field(index=True)  # session id of the user
    # duration of the user on the page
    duration: Optional[int] = Field(default=0)
    # id: Optional[int] | None = Field(default=None, primary_key=True)
    # id: int  # required field
    # sensor_id: int  # avg value of a sensor at any given time
    # page: Optional[str] = ""  # optional field
    # indexes decribe /about, /contact, /home, etc.
    # description: Optional[str] = ""  # optional field
    # # created_at: datetime = Field(
    # #     default_factory=get_utc_now,
    # #     sa_type=sqlmodel.DateTime(timezone=True),
    # #     nullable=False
    # # )
    # updated_at: datetime = Field(
    #     default_factory=get_utc_now,
    #     sa_type=sqlmodel.DateTime(timezone=True),
    #     nullable=False
    # )

    # the interval of time between chunks of data
    __chunk_time_interval__ = "INTERVAL 1 day"
    # the interval of time after which the data is dropped/deleted
    __drop_after__ = "INTERVAL 3 months"


class EventCreateSchema(SQLModel):
    page: str
    user_agent: Optional[str] = Field(default="")
    ip_address: Optional[str] = Field(default="")
    referrer: Optional[str] = Field(default="")
    session_id: Optional[str] = Field(default="")
    duration: Optional[int] = Field(default=0)
    # page: str
    # description: Optional[str] = Field(default="")  # optional field


# class EventUpdateSchema(SQLModel):
#     description: str


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventBucketSchema(SQLModel):
    bucket: datetime
    page: str
    user_agent: Optional[str] = ""
    operating_system: Optional[str] = ""
    avg_duration: Optional[float] = 0.0
    count: int
