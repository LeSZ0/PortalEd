from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from portaled.queries.user import authenticate_user
from portaled.database.db import DBSession
from portaled.utils.errors import UnauthorizedError, InvalidToken, NotFoundError
from portaled.auth.utils import create_access_token, verify_token, refresh_token
from portaled.schemas.user import UserSchema
from portaled.schemas.profile import ProfileSchema
from portaled.auth.responses import TokenResponse
from portaled.auth.schemas import LoginSchema


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token")
async def generate_access_token(
    db: DBSession, form_data: OAuth2PasswordRequestForm = Depends()
):
    authenticated_user = await authenticate_user(
        db=db, password=form_data.password, username=form_data.username
    )

    profiles = list()
    if authenticated_user.profiles:
        for profile in authenticated_user.profiles:
            profile = ProfileSchema(
                id=profile.id,
                role=profile.role,
                created_at=profile.created_at,
                user_id=profile.user_id,
            )
            profiles.append(profile)

    user = UserSchema(
        id=authenticated_user.id,
        username=authenticated_user.username,
        email=authenticated_user.email,
        full_name=authenticated_user.full_name,
        birth_date=authenticated_user.birth_date,
        dni=authenticated_user.dni,
        profile=profiles if authenticated_user.profiles else None,
        created_at=authenticated_user.created_at,
        is_active=authenticated_user.is_active,
    )

    access_token = await create_access_token(subject=user)
    return TokenResponse(access_token=access_token)


@auth_router.post("/login", response_model=TokenResponse)
async def login(db: DBSession, schema: LoginSchema):
    authenticated_user = await authenticate_user(
        db=db, username=schema.username, password=schema.password, email=schema.email
    )
    user = UserSchema(**authenticated_user.__dict__)
    access_token = await create_access_token(subject=user)
    refresh_token = await create_access_token(subject=user, refresh_token=True)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@auth_router.post("/token/verify")
async def verify_user_token(token: str):
    try:
        user = await verify_token(token)
        return user
    except InvalidToken as e:
        raise HTTPException(status_code=e.status_code, detail=e.msg)


@auth_router.post("/token/refresh")
async def refresh_access_token(token: str):
    new_access_token = await refresh_token(token)
    return TokenResponse(access_token=new_access_token)

