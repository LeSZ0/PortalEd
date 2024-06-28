from pydantic import BaseModel, Field
from typing import Optional


class TokenResponse(BaseModel):
    access_token: str = Field()
    refresh_token: Optional[str] = Field(default=None)
    token_type: str = Field(default="bearer")
