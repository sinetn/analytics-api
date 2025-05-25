from api.db.config import DATABASE_URL
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from .models import (
    EventModel,
    EventCreateSchema,
    # EventUpdateSchema,
    EventBucketSchema,
    # EventListSchema,
    get_utc_now
)
from api.db.session import get_session
from sqlmodel import Session, select
from timescaledb.hyperfunctions import time_bucket
from sqlalchemy import func, case
from datetime import datetime, timedelta, timezone
from typing import List


router = APIRouter()

# Get data here
# List View
# GET /api/events

DEFAULT_LOOKUP_PAGES = [
    "/", "/about", "/pricing", "/contact",
    "/blog", "/products", "/login", "/signup",
    "/dashboard", "/settings"]


@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="1 day"),
    pages: List = Query(default=None),
    session: Session = Depends(get_session)
):
    # print(os.environ.get("DATABASE_URL", DATABASE_URL))
    # query = select(EventModel).order_by(EventModel.updated_at.asc()).limit(
    #     10)                 # limit the number of rows and change the order
    os_case = case(
        (EventModel.user_agent.ilike("%windows%"), "Windows"),
        (EventModel.user_agent.ilike("%macintosh%"), "MacOS"),
        (EventModel.user_agent.ilike("%iphone%"), "iOS"),
        (EventModel.user_agent.ilike("%android%"), "Android"),
        (EventModel.user_agent.ilike("%linux%"), "Linux"),
        else_="Other"
    ).label("operating_system")
    bucket = time_bucket(duration, EventModel.time)
    # you can comment out the pages you don't want to see
    lookup_pages = pages if isinstance(pages, list) and len(
        pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label("bucket"),
            os_case,
            EventModel.page.label("page"),
            func.avg(EventModel.duration).label("avg_duration"),
            func.count().label("count")  # we can label it if we want using: .label("event_count")

        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            os_case,
            EventModel.page,
        )
        .order_by(
            bucket,
            os_case,
            EventModel.page
        )
    )
    results = session.exec(query).fetchall()
    return results
    # return {
    #     # a bunch of items in a table
    #     "results": results,
    #     "count": len(results)
    # }

# SEND DATA HERE
# Create View
# POST /api/events


@router.post("/", response_model=EventModel)
def create_event(
        payload: EventCreateSchema,
        session: Session = Depends(get_session)):
    data = payload.model_dump()  # payload to dict using pydantic
    obj = EventModel.model_validate(data)
    session.add(obj)  # preparing to add to the database
    session.commit()  # actually add to the database
    session.refresh(obj)  # refresh the object to get the id, to get id ...
    return obj

# GET /api/events/123


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result
    # { if you are not returning dictionaries do not use {}
    #     # # a single row
    #     # "id": event_id

    # }


# @router.put("/{event_id}", response_model=EventModel)
# def update_event(
#         event_id: int,
#         payload: EventUpdateSchema,
#         session: Session = Depends(get_session)):

#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found")

#     data = payload.model_dump()
#     for key, value in data.items():
#         setattr(obj, key, value)
#     obj.updated_at = get_utc_now()
#     session.add(obj)  # preparing to add to the database
#     session.commit()  # actually add to the database
#     session.refresh(obj)  # refresh the object to get the id, to get id ...
#     return obj
#     # {
#     #     # a single row
#     #     "id": event_id,
#     #     **data
#     # }


# @router.delete("/{event_id}", response_model=EventModel)
# def delete_event(event_id: int, session: Session = Depends(get_session)):
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found")

#     session.delete(obj)
#     session.commit()
#     return obj
