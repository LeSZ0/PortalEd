from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models.event import Event
from portaled.schemas.event import EventCreateSchema, EventUpdateSchema
from portaled.utils.errors import NotFoundError
from datetime import date
from typing import Optional


def get_event(db: Session, event_id: UUID) -> Event | None:
    """Get an event by id

    Method for quering the database and get an event by id
    """
    event = db.get(Event, event_id)
    if not event:
        raise NotFoundError("Event not found")

    return event


def get_events(
    db: Session,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    user_id: Optional[UUID] = None,
) -> list[Event]:
    """Get a list of comments

    Method for quering the database and get a list of comments.
    """

    main_query = db.query(Event)

    if from_date:
        main_query.filter(Event.event_date >= from_date)
    if to_date:
        main_query.filter(Event.event_date <= to_date)
    if user_id:
        main_query.filter(Event.user_id == user_id)

    return main_query.order_by(Event.updated_at).all()


def create_event(db: Session, user_id: UUID, event: EventCreateSchema) -> Event:
    """Create an event

    Method for quering the database and creating a new event.
    """
    db_event = Event(
        id=event.id,
        title=event.title,
        description=event.description,
        meeting_link=event.meeting_link,
        event_date=event.event_date,
        event_time=event.event_time,
        created_at=event.created_at,
        updated_at=event.updated_at,
        user_id=user_id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: UUID, event: EventUpdateSchema) -> Event:
    update_query = (
        update(Event).where(Event.id == event_id).values(**event.model_dump())
    )
    db.execute(update_query)
    db.commit()
    db_event = get_event(db, event_id)
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: UUID) -> str:
    delete_query = delete(Event).where(Event.id == event_id)
    db.execute(delete_query)
    db.commit()

    return "Event deleted successfuly"
