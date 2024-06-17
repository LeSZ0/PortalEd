from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional


class GradeSchema(BaseModel):
    id: int
    name: str
    observations: str
    institution_id: int


class GradeCreateSchema(BaseModel):
    name: str = Field()
    observations: str = Field()
    institution_id: int = Field()


class GradeUpdateSchema(BaseModel):
    name: Optional[str] = None
    observations: Optional[str] = None
