from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from portaled.schemas.event import EventSchema, EventCreateSchema, EventUpdateSchema
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.event as queries
from portaled.auth.utils import verify_token
from portaled.auth.dependencies import AuthorizatedUser
from uuid import UUID


event_apis = APIRouter(
    prefix="/events", tags=["events"], dependencies=[Depends(verify_token)]
)


@event_apis.get("", response_model=list[EventSchema])
def get_events(db: Session = Depends(get_db)) -> list[EventSchema]:
    events = queries.get_events(db=db)
    return events


@event_apis.post("", response_model=EventSchema, status_code=201)
def create_event(
    user: AuthorizatedUser, event: EventCreateSchema, db: Session = Depends(get_db)
) -> EventSchema:
    db_event = queries.create_event(db=db, user_id=user.id, event=event)
    return db_event


@event_apis.get("/{event_id}", response_model=EventSchema, name="Event details")
def get_event_by_id(event_id: UUID, db: Session = Depends(get_db)) -> EventSchema:
    event = queries.get_event(db=db, event_id=event_id)
    return event


@event_apis.put("/{event_id}", response_model=EventSchema)
def update_event(
    event_id: UUID, event: EventUpdateSchema, db: Session = Depends(get_db)
) -> EventSchema:
    db_event = queries.update_event(db=db, event_id=event_id, event=event)
    return db_event


@event_apis.delete("/{event_id}", response_class=JSONResponse)
def delete_event(event_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    msg = queries.delete_event(db=db, event_id=event_id)
    return JSONResponse(msg, status_code=202)
