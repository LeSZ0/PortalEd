from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    Date,
    Text,
    Time,
    UUID,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from portaled.database import db
from datetime import date, time, datetime, timezone
from portaled.models.user import User
import uuid
from typing import Optional


class Event(db.Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    meeting_link: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    event_date: Mapped[date] = mapped_column(Date)
    event_time: Mapped[time] = mapped_column(Time)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    institution = relationship("Institution", backref="event")
    created_by: Mapped[User] = relationship(User, backref="event")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
