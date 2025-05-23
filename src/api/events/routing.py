from api.db.config import DATABASE_URL
import os
from fastapi import APIRouter, Depends, HTTPException
from .models import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)
from api.db.session import get_session
from sqlmodel import Session, select

router = APIRouter()

# Get data here
# List View
# GET /api/events


@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # print(os.environ.get("DATABASE_URL", DATABASE_URL))
    query = select(EventModel).order_by(EventModel.id.desc()
                                        # limit the number of rows and change the order
                                        ).limit(10)
    results = session.exec(query).all()
    return {
        # a bunch of items in a table
        "results": results,
        "count": len(results)
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


@router.put("/{event_id}", response_model=EventModel)
def update_event(
        event_id: int,
        payload: EventUpdateSchema,
        session: Session = Depends(get_session)):

    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")

    data = payload.model_dump()
    for key, value in data.items():
        setattr(obj, key, value)
    session.add(obj)  # preparing to add to the database
    session.commit()  # actually add to the database
    session.refresh(obj)  # refresh the object to get the id, to get id ...
    return obj
    # {
    #     # a single row
    #     "id": event_id,
    #     **data
    # }


@router.delete("/{event_id}", response_model=EventModel)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(obj)
    session.commit()
    return obj
