from pydantic import BaseModel, Field
from datetime import datetime, timezone
from portaled.utils.code_generator import generate_random_code
from portaled.schemas.grade import GradeSchema, GradeCreateSchema, GradeUpdateSchema
from typing import Optional


class InstitutionSchema(BaseModel):
    id: int
    code: str
    name: str
    short_name: str
    address: str
    type: str
    created_at: datetime
    updated_at: datetime


class InstitutionCreateSchema(BaseModel):
    name: str = Field()
    short_name: str = Field()
    address: str = Field()
    type: str = Field()

    @property
    def code(self) -> str:
        unique_code = f"{self.short_name}_{int(datetime.now().timestamp())}"
        return unique_code

    @property
    def is_active(self) -> bool:
        return True


class InstitutionUpdateSchema(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    address: Optional[str] = None
    type: Optional[str] = None
