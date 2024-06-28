import uuid
from pydantic import BaseModel, Field, EmailStr, field_validator
from portaled.utils.secret_field import SecretField
from portaled.schemas.profile import ProfileCreateSchema, UserProfileSchema
from typing import Optional
from datetime import datetime, timezone, date


class UserSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    full_name: str
    birth_date: date
    dni: str
    profiles: Optional[list[UserProfileSchema]] = None
    created_at: datetime
    is_active: bool


class UserCreateSchema(BaseModel):
    username: str = Field()
    password: SecretField = Field()
    email: EmailStr = Field()
    full_name: str = Field()
    birth_date: date = Field()
    dni: str = Field()
    superuser: Optional[bool] = None

    @property
    def is_active(self) -> bool:
        return True

    @field_validator('dni')
    def validate_dni(cls, value):
        if len(value) < 8:
            raise ValueError("DNI must be at least 8 digits long")
        return value


class UserUpdateSchema(BaseModel):
    username: str = Field()
    email: EmailStr = Field()
    full_name: str = Field()
    birth_date: date = Field()
    dni: str = Field()

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)

    @field_validator('dni')
    def validate_dni(cls, value):
        if len(value) < 8:
            raise ValueError("DNI must be at least 8 digits long")
        return value


class UserPartialUpdateSchema(BaseModel):
    username: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)


class UserProfilesToAddSchema(BaseModel):
    profiles: Optional[list[ProfileCreateSchema]] = Field(default_factory=list)

    @property
    def updated_at(self) -> datetime:
        return datetime.now(timezone.utc)
