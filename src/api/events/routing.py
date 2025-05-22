from fastapi import APIRouter
from .schemas import (
    EventSchema,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

# Get data here
# List View
# GET /api/events


@router.get("/")
def read_events() -> EventListSchema:
    return {
        # a bunch of items in a table
        "results": [{"id": 1}, {"id": 2}, {"id": 3}],
        "count": 3
    }

# SEND DATA HERE
# Create View
# POST /api/events


@router.post("/")
def create_events(payload: EventCreateSchema) -> EventSchema:
    data = payload.model_dump()  # payload to dict using pydantic
    return {
        # a single row
        "id": 123,
        **data  # unpacking the dict
    }

# GET /api/events/123


@router.get("/{event_id}")
def get_event(event_id: int) -> EventSchema:
    return {
        # a single row
        "id": event_id
    }


@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventSchema:
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
