from api.db.config import DATABASE_URL
import os
from fastapi import APIRouter, Depends
from .models import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)
from api.db.session import get_session
from sqlmodel import Session

router = APIRouter()

# Get data here
# List View
# GET /api/events


@router.get("/")
def read_events() -> EventListSchema:
    print(os.environ.get("DATABASE_URL", DATABASE_URL))
    return {
        # a bunch of items in a table
        "results": [{"id": 1}, {"id": 2}, {"id": 3}],
        "count": 3
    }

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


@router.get("/{event_id}")
def get_event(event_id: int) -> EventModel:
    return {
        # a single row
        "id": event_id
    }


@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    data = payload.model_dump()
    return {
        # a single row
        "id": event_id,
        **data
    }

# @router.delete("/{event_id}")
# def delete_event(event_id: int) -> EventSchema:
#     return {
#         # a single row
#         "id": event_id
#     }
