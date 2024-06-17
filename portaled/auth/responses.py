from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field()
    token_type: str = Field(default="bearer")
