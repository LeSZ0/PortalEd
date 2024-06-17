from pydantic import BaseModel, Field, FileUrl
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional
from portaled.schemas.category import CategorySchema
from portaled.schemas.user import UserSchema


class DocumentSchema(BaseModel):
    id: UUID
    name: str
    slug: str
    url: FileUrl
    category: CategorySchema
    created_at: datetime
    created_by: UserSchema


class DocumentCreateSchema(BaseModel):
    name: str = Field()
    url: FileUrl = Field()
    category_id: int = Field()

    @property
    def id(self) -> UUID:
        return uuid4()

    @property
    def slug(self) -> str:
        name_slugged = self.name.lower().replace(" ", "-")
        return name_slugged

    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)


class DocumentUpdateSchema(BaseModel):
    name: str = Field()
    url: FileUrl = Field()
    category: CategorySchema = Field()

    @property
    def slug(self) -> str:
        name_slugged = self.name.lower().replace(" ", "-")
        return name_slugged
