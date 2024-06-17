from sqlalchemy import (
    Integer,
    String,
    Boolean,
    UUID,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from portaled.database import db
from portaled.models.profile_grade import profile_grade_table
from datetime import datetime, timezone
import uuid


class Profile(db.Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4(), unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))

    role: Mapped[str] = mapped_column(String)
    grades = relationship(
        "Grade", secondary=profile_grade_table, back_populates="profiles"
    )
    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey("institutions.id"))
    institution = relationship("Institution", backref="profile")
    is_active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
