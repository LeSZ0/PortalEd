from pydantic import BaseModel, Field
from datetime import datetime, timezone


class CategorySchema(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime


class CategoryCreateSchema(BaseModel):
    name: str = Field()

    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def slug(self) -> str:
        name_slugged = self.name.lower().replace(" ", "-")
        return name_slugged

    @property
    def is_active(self) -> bool:
        return True


class CategoryUpdateSchema(BaseModel):
    name: str = Field()

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def slug(self) -> str:
        name_slugged = self.name.lower().replace(" ", "-")
        return name_slugged
