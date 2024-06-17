from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from portaled.database import db
from datetime import datetime, timezone
from portaled.models.user_institution import user_institution_table


class Institution(db.Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(length=10), index=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    short_name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    users = relationship(
        "User", secondary=user_institution_table, back_populates="institutions"
    )
    is_active: Mapped[bool] = mapped_column(Boolean)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
