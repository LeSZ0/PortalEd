from passlib.context import CryptContext
from portaled.models.user import User
from portaled.schemas.user import UserSchema
from datetime import timedelta, datetime, timezone
from typing import Optional, Any
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from portaled.utils.errors import InvalidToken
from typing import Annotated
from portaled.utils.get_env import getenv


oaut2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_credentials(password: str, user: User) -> bool:
    """Checks if the user credentials are correct.

    This util function checks if the user credentials are correct
    """
    if not password_context.verify(password, user.password):
        return False

    return True


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expiration_time = datetime.now(timezone.utc) + expires_delta
    else:
        expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=int(getenv("TOKEN_EXPIRATION_MINUTES"))
        )

    data_to_encode.update({"exp": expiration_time})
    encoded_jwt = jwt.encode(
        data_to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM")
    )
    return encoded_jwt


async def verify_token(
    token: Annotated[str, Depends(oaut2_scheme)]
) -> UserSchema | InvalidToken:
    try:
        payload = jwt.decode(
            token=token, key=getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")]
        )
        if "user" not in payload:
            raise InvalidToken()

        if not payload["user_active"]:
            raise InvalidToken()

        return UserSchema(**payload["user"])

    except JWTError:
        raise InvalidToken()
