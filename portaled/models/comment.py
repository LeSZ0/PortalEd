from sqlalchemy import Integer, ForeignKey, DateTime, Text, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from portaled.database import db
from datetime import datetime, timezone
from portaled.models.user import User
from portaled.models.post import Post
import uuid


class Comment(db.Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text)
    post: Mapped[Post] = relationship("Post", backref="comment_post")
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    author: Mapped[User] = relationship("User", backref="author")
    author_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))
