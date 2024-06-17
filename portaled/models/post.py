from sqlalchemy import Column, Table, Integer, String, ForeignKey, DateTime, Text, UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func
from portaled.database import db
from datetime import datetime, timezone
from portaled.models.user import User
from portaled.models.institution import Institution


class Tag(db.Base):
    __tablename__ = "tags"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, unique=True, nullable=False)


posts_tags_table = Table(
    "post_tags",
    db.Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Post(db.Base):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(length=200), index=True)
    slug: str = Column(String, index=True)
    body: str = Column(Text)
    tags = relationship("Tag", secondary=posts_tags_table, backref="post")
    post_tags = association_proxy("tags", "name")
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"))
    institution = relationship(Institution, backref="post")
    author_id = Column(UUID, ForeignKey("users.id"))
    author = relationship(User, backref="posts")
    created_at: datetime = Column(DateTime, server_default=func.now())
    updated_at: datetime = Column(DateTime, default=datetime.now(timezone.utc))
