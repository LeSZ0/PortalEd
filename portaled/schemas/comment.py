from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID
from portaled.schemas.user import UserSchema


class CommentSchema(BaseModel):
    id: int
    message: str
    post_id: int
    updated_at: datetime
    author: UserSchema


class CommentCreateSchema(BaseModel):
    message: str = Field()
    post_id: int = Field()

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)


class CommentUpdateSchema(BaseModel):
    message: str = Field()

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)
