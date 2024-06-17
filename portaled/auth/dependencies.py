from fastapi import Depends
from portaled.auth.utils import verify_token
from typing import Annotated
from portaled.schemas.user import UserSchema


AuthorizatedUser = Annotated[UserSchema, Depends(verify_token)]
