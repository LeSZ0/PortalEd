from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update
from portaled.models.user import User
from portaled.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
    UserProfilesToAddSchema,
)
from portaled.utils.errors import NotFoundError, AlreadyExistError, UnauthorizedError
from portaled.auth.utils import password_context, check_credentials
from typing import Optional
from fastapi import Depends
from portaled.database.db import get_db
from portaled.queries.profile import create_profile


def get_user(
    db: Session,
    user_id: Optional[UUID] = None,
    search_by: Optional[tuple[str, str]] = None,
) -> User | None:
    """Get a user by id

    Method for quering the database and get a user by the provided id.
    If the param :search_by: is provided, it will try to search a user using that field
    """
    if search_by:
        field, value = search_by
        user = db.query(User).filter(getattr(User, field) == value).first()
        if not user:
            raise NotFoundError("User not found")
        return user
    
    user = db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    return db.get(User, user_id)


def get_users(db: Session, get_all: bool = False) -> list[User]:
    """Get a list of users

    Method for quering the database and get a list of users.
    If get_all is True, all of the existing users will be returned,
    otherwise, the query will get only the active ones.
    """
    if get_all:
        return db.query(User).order_by(User.username).all()

    return db.query(User).filter(User.is_active == True).order_by(User.username)


def create_user(db: Session, user: UserCreateSchema) -> User | AlreadyExistError:
    """Create a user

    Method for quering the database and create a user
    """
    if db_user := db.query(User).filter(User.email == user.email).first():
        if db_user.is_active:
            raise AlreadyExistError("User already exists.")
        db_user.is_active = True
        if db_user.profile:
            db_user.profile.is_active = True
    else:
        hashed_password = password_context.hash(user.password.get_secret_value())
        db_user = User(**user.model_dump())
        db_user.is_active = user.is_active
        db_user.password = hashed_password
        db_user.profiles = list()

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: UUID, user: UserUpdateSchema) -> User:
    """Update an user

    This method is for updating a specific user
    """
    update_query = update(User).where(User.id == user_id).values(**user.model_dump())
    db.execute(update_query)
    db.commit()
    db_user = get_user(db, user_id)
    db.refresh(db_user)
    return db_user


def add_profiles_to_user(db: Session, user_id: UUID, schema: UserProfilesToAddSchema) -> User:
    db_user = get_user(db, user_id=user_id)
    for user_profile in schema.profiles:
        profile = create_profile(db=db, profile=user_profile, user=db_user)
        db_user.profiles.append(profile)

    db.commit()
    db.refresh(db_user)
    return db_user


def patch_user(db: Session, user_id: UUID, user: UserPartialUpdateSchema) -> User:
    """Partially Update an user

    This method is for partially updating a specific user
    """
    data = user.model_dump(exclude_unset=True)
    db_user: User = get_user(db, user_id)
    for key, value in data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID) -> str | NotFoundError:
    """Delete an user

    This method is for deleting a user.
    This is a logical deletion, not phisical.
    """
    user = get_user(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    user.is_active = False
    if user.profile:
        user.profile.is_active = False
    db.commit()
    db.refresh(user)
    return "User deleted successfuly"


def authenticate_user(
    db: Session,
    password: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
) -> User | UnauthorizedError:
    """Authenticate the user

    This method is for authenticating a user.
    User provided username and password, a check runs to see if the credentials matches.
    """
    if username:
        search_by = ("username", username)
    if email:
        search_by = ("email", email)

    user = get_user(db=db, search_by=search_by)
    if not user.is_active:
        raise NotFoundError("User does not exist")

    valid_credentials = check_credentials(password, user)
    if not valid_credentials:
        raise UnauthorizedError()

    return user
