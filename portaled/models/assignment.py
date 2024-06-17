from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, Float, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from portaled.database import db
from portaled.models.grade import Grade
from portaled.models.user import User
import uuid
from datetime import datetime, timezone


class Assignment(db.Base):
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
    identifier: Mapped[str] = mapped_column(String, unique=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    grade_id: Mapped[int] = mapped_column(Integer, ForeignKey("grades.id"))
    grade: Mapped[Grade] = relationship("Grade", backref="assignment")
    deadline: Mapped[datetime] = mapped_column(DateTime)
    score_to_approve: Mapped[float] = mapped_column(Float(precision=2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    created_by: Mapped[User] = relationship("User", backref="assignment_created")
    crated_by_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))
