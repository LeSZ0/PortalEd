from pydantic import BaseModel, Field
from datetime import datetime, timezone, date, time
from uuid import UUID, uuid4
from typing import Optional


class EventSchema(BaseModel):
    id: UUID
    title: str
    description: str
    meeting_link: Optional[str]
    event_date: date
    event_time: time
    user_id: UUID
    updated_at: datetime


class EventCreateSchema(BaseModel):
    title: str = Field()
    description: str = Field()
    meeting_link: Optional[str] = Field(default=None)
    event_date: date = Field()
    event_time: time = Field()

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def id(self) -> UUID:
        return uuid4()


class EventUpdateSchema(BaseModel):
    title: str = Field()
    description: str = Field()
    meeting_link: Optional[str] = Field()
    event_date: date = Field()
    event_time: time = Field()

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)
