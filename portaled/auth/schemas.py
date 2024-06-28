from pydantic import BaseModel, Field
from typing import Optional


class LoginSchema(BaseModel):
    username: str = Field()
    password: str = Field()
    email: Optional[str] = None
