from pydantic import BaseModel, Field
from datetime import datetime, timezone
from portaled.schemas.institution import InstitutionSchema
from portaled.schemas.grade import GradeSchema
from portaled.schemas.user import UserSchema
from uuid import UUID
from typing import Optional


class AnnouncementSchema(BaseModel):
    id: UUID
    title: str
    description: str
    institution: InstitutionSchema
    grade: Optional[GradeSchema] = None
    created_at: datetime
    updated_at: datetime
    # created_by: UserSchema


class AnnouncementCreateSchema(BaseModel):
    title: str = Field()
    description: str = Field()
    institution_id: int = Field()
    grade_id: Optional[int] = Field(default=None)


class AnnouncementUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
