from sqlalchemy import Integer, String, ForeignKey, Text, DateTime, Float, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from portaled.database import db
from portaled.utils.enums import Statuses
import uuid
from datetime import datetime, timezone


class AssignmentResolution(db.Base):
    __tablename__ = "assignments_resolutions"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid.uuid4())
    assignment_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("assignments.id"), nullable=False)
    assignment = relationship("Assignment", backref="resolution")
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="assignment_resolution")
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default=Statuses.PENDING)
    score: Mapped[float] = mapped_column(Float)
    approved: Mapped[bool] = mapped_column(Boolean)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    feedback: Mapped[str] = mapped_column(Text, nullable=True)
    evaluation_criteria: Mapped[str] = mapped_column(Text, nullable=True)
    # attachments: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    class History(db.Base):
        __tablename__ = "assignments_resolutions_history"

        id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, unique=True, default=uuid.uuid4())
        resolution_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("assignments_resolutions.id"), nullable=False, index=True)
        resolution = relationship("AssignmentResolution", backref="history")
        revision_number: Mapped[int] = mapped_column(Integer, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

        content: Mapped[str] = mapped_column(Text)
        status: Mapped[str] = mapped_column(String, default=Statuses.PENDING)
        score: Mapped[float] = mapped_column(Float)
        approved: Mapped[bool] = mapped_column(Boolean)
        feedback: Mapped[str] = mapped_column(Text, nullable=True)
        evaluation_criteria: Mapped[str] = mapped_column(Text, nullable=True)
