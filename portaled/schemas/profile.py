import uuid
from pydantic import BaseModel, Field
from datetime import date, datetime, timezone
from typing import Optional
from portaled.utils.enums import Role
from portaled.schemas.institution import InstitutionSchema
from portaled.schemas.grade import GradeSchema


class ProfileSchema(BaseModel):
    id: uuid.UUID
    role: Role
    created_at: datetime
    user_id: uuid.UUID
    institution: Optional[InstitutionSchema] = None
    grades: Optional[list[GradeSchema]] = None


class UserProfileSchema(BaseModel):
    id: uuid.UUID
    role: Role
    created_at: datetime
    institutions: Optional[list[InstitutionSchema]] = None
    grades: Optional[list[GradeSchema]] = None


class ProfileCreateSchema(BaseModel):
    role: Role = Field()
    institution_id: int = Field()
    grades: list[GradeSchema] = Field(default_factory=list)
    user_id: uuid.UUID = Field()

    @property
    def id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def created_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @property
    def is_active(self) -> bool:
        if self.role == Role.MANAGEMENT:
            return True

        return False


class ProfileUpdateSchema(BaseModel):
    role: Optional[Role] = None
    institutions: Optional[list[int]] = None
    grades: Optional[list[int]] = None


class ProfilePartialUpdateSchema(BaseModel):
    role: Optional[Role] = None
