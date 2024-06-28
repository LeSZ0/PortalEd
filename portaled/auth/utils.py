from passlib.context import CryptContext
from portaled.models.user import User
from portaled.schemas.user import UserSchema
from datetime import timedelta, datetime, timezone
from typing import Optional, Any
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from portaled.utils.errors import InvalidToken, UnauthorizedError
from typing import Annotated
from portaled.utils.get_env import getenv
import json


oaut2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def check_credentials(password: str, user: User) -> bool:
    """Checks if the user credentials are correct.

    This util function checks if the user credentials are correct
    """
    if not password_context.verify(password, user.password):
        return False

    return True


async def create_access_token(subject: UserSchema, expires_delta: Optional[timedelta] = None, refresh_token: bool = False) -> str:
    if not subject.is_active:
        raise UnauthorizedError("User does not exist")
    
    if expires_delta:
        expiration_time = datetime.now(timezone.utc) + expires_delta
    else:
        token_expire_minutes = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        if refresh_token:
            token_expire_minutes = int(getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

        expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=token_expire_minutes
        )

    data = {
        "user": subject.model_dump_json(),
        "exp": expiration_time
    }
    encoded_jwt = jwt.encode(
        data, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM")
    )
    return encoded_jwt


async def verify_token(
    token: Annotated[str, Depends(oaut2_scheme)]
) -> UserSchema | InvalidToken:
    try:
        user, expiration_time = await decode_access_token(token)
        if not user:
            raise InvalidToken()

        if not user.is_active:
            raise InvalidToken()

        if expiration_time:
            expiration_date = datetime.fromtimestamp(expiration_time, timezone.utc)
            if expiration_date <= datetime.now(timezone.utc):
                raise InvalidToken()

        return user

    except JWTError:
        raise InvalidToken()
    

async def decode_access_token(token: str) -> tuple[UserSchema, str]:
    payload = jwt.decode(
        token=token, key=getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")]
    )

    return UserSchema(**json.loads(payload.get("user"))), payload.get("exp")


async def refresh_token(refresh_token: Annotated[str, Depends(oaut2_scheme)]) -> str:
    try:
        user = await verify_token(refresh_token)

        if not user.is_active:
            raise UnauthorizedError()
    
        access_token = await create_access_token(subject=user)
        return access_token
    except JWTError:
        raise InvalidToken()
