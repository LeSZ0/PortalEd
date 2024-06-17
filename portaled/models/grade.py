from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from portaled.database import db
from portaled.models.profile_grade import profile_grade_table
from datetime import datetime, timezone


class Grade(db.Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    observations: Mapped[str] = mapped_column(String, nullable=True)
    institution_id: Mapped[int] = mapped_column(Integer, ForeignKey("institutions.id"))
    institution = relationship("Institution", backref="institution")
    profiles = relationship(
        "Profile", secondary=profile_grade_table, back_populates="grades"
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
