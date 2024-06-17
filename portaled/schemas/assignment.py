from pydantic import BaseModel, Field
from datetime import datetime
from portaled.schemas import GradeSchema, UserSchema
from uuid import UUID
from typing import Optional


class AssignmentSchema(BaseModel):
    id: UUID
    identifier: str
    title: str
    description: str
    grade: GradeSchema
    deadline: datetime
    score_to_approve: float
    created_at: datetime
    updated_at: datetime
    created_by: UserSchema


class AssignmentCreateSchema(BaseModel):
    identifier: str = Field()
    title: str = Field()
    description: str = Field()
    grade_id: int = Field()
    deadline: datetime = Field()
    score_to_approve: float = Field()


class AssignmentUpdateSchema(BaseModel):
    identifier: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    grade_id: Optional[int] = None
    deadline: Optional[datetime] = None
    score_to_approve: Optional[float] = None
