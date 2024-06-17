from sqlalchemy import String, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from portaled.database import db
from datetime import datetime, timezone
from portaled.models.user import User
from portaled.models.category import Category
import uuid


class Document(db.Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    category: Mapped[Category] = relationship(Category, backref="document_category")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    created_by: Mapped[User] = relationship(User, backref="document_created_by")
    created_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))

    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    institution = relationship("Institution", backref="document")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
