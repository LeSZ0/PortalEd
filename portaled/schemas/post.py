from pydantic import BaseModel, Field
from portaled.schemas.user import UserSchema
from portaled.schemas.institution import InstitutionSchema
from datetime import datetime, timezone
from uuid import UUID


class TagFullSchema(BaseModel):
    id: int = Field()
    name: str = Field()


class PostSchema(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    post_tags: list[str]
    institution: InstitutionSchema
    author: UserSchema
    last_update: datetime


class PostCreateSchema(BaseModel):
    title: str = Field(max_length=200)
    slug: str = Field()
    body: str = Field()
    tags: list[str] = Field(default_factory=list)
    institution_id: int = Field()
    author_id: UUID = Field()

    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def last_update(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def slug(self) -> str:
        slug_str = self.title.lower().replace(" ", "-")
        return slug_str


class PostUpdateSchema(BaseModel):
    title: str = Field(max_length=200)
    body: str = Field()

    @property
    def last_update(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def slug(self) -> str:
        slug_str = self.title.lower().replace(" ", "-")
        return slug_str
