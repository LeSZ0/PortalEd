from sqlalchemy import String, Boolean, UUID, DateTime, Date
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from portaled.database import db
from portaled.models.user_institution import user_institution_table
from datetime import date, datetime, timezone
import uuid


class User(db.Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4(), unique=True)
    username: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    full_name: Mapped[str] = mapped_column(String)
    dni: Mapped[str] = mapped_column(String, index=True)
    birth_date: Mapped[date] = mapped_column(Date)
    profiles = relationship("Profile")
    institutions = relationship(
        "Institution", secondary=user_institution_table, back_populates="users"
    )
    superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
