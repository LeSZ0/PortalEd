from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from uuid import UUID
from portaled.schemas.user import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
)
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.user as queries
from typing import Annotated
from portaled.auth.utils import verify_token


user_apis = APIRouter(prefix="/users", tags=["users"])


@user_apis.get(
    path="", response_model=list[UserSchema], dependencies=[Depends(verify_token)]
)
async def get_users(
    db: Session = Depends(get_db),
    getall: Annotated[bool | None, Query(description="get all users")] = None,
) -> list[UserSchema]:
    user = queries.get_users(db, getall)
    return user


@user_apis.post("", response_model=UserSchema)
async def create_user(
    user: UserCreateSchema, db: Session = Depends(get_db)
) -> UserSchema:
    db_user = queries.create_user(db, user)
    return db_user

@user_apis.get(
    path="/{user_id}",
    response_model=UserSchema,
    name="Get user",
    dependencies=[Depends(verify_token)],
)
async def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)) -> UserSchema:
    user = queries.get_user(db, user_id)
    return user


@user_apis.put(
    path="/{user_id}", response_model=UserSchema, dependencies=[Depends(verify_token)]
)
async def update_user(
    user_id: UUID, user: UserUpdateSchema, db: Session = Depends(get_db)
) -> UserSchema:
    db_user = queries.update_user(db=db, user_id=user_id, user=user)
    return db_user


@user_apis.patch(
    path="/{user_id}", response_model=UserSchema, dependencies=[Depends(verify_token)]
)
async def patch_user(
    user_id: UUID, user: UserPartialUpdateSchema, db: Session = Depends(get_db)
) -> UserSchema:
    db_user = queries.patch_user(db=db, user_id=user_id, user=user)
    return db_user


@user_apis.delete("/{user_id}", dependencies=[Depends(verify_token)])
async def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    queries.delete_user(db, user_id)
    return JSONResponse("User deleted successfuly", status_code=202)
