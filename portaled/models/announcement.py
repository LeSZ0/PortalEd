from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship
from sqlalchemy.sql import func
from portaled.database import db
import uuid
from datetime import datetime, timezone


class Announcement(db.Base):
    __tablename__ = "announcements"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4(), unique=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey("institutions.id"))
    institution = relationship("Institution", backref="announcement")
    grade_id: Mapped[int] = mapped_column(Integer, ForeignKey("grades.id"), nullable=True)
    grade = relationship("Grade", backref="announcement")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    created_by = relationship("User", backref="announcement")
    created_by_id = mapped_column(UUID, ForeignKey("users.id"))
