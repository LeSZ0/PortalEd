from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import update
from portaled.models.profile import Profile
from portaled.models.user import User
from portaled.schemas.profile import (
    ProfileCreateSchema,
    ProfileUpdateSchema,
    ProfilePartialUpdateSchema,
)
from portaled.utils.errors import NotFoundError
from typing import Optional


def get_profile(db: Session, profile_id: UUID) -> Profile | None:
    """Get a profile by id

    Method for quering the database and get a profile by id
    """
    profile = db.get(Profile, profile_id)
    if not profile:
        raise NotFoundError("Profile not found")

    return profile


def get_profiles(db: Session, get_all: bool = False) -> list[Profile]:
    """Get a list of profiles

    Method for quering the database and get a list of profiles.
    If get_all is True, all of the existing profiles will be returned,
    otherwise, the query will get only the active ones.
    """
    if get_all:
        return db.query(Profile).all()

    return (
        db.query(Profile).filter(Profile.is_active == True)
    )


def create_profile(db: Session, profile: ProfileCreateSchema, user: Optional[User] = None):
    user_id = user.id if user else profile.user_id
    if db_profile := db.query(Profile).filter(Profile.user_id == user_id).first():
        db_profile.is_active = True
    else:
        db_profile = Profile(
            institution_id=profile.institution_id,
            role=profile.role,
            is_active=profile.is_active,
            created_at=profile.created_at,
            user_id=user_id
        )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(
    db: Session,
    profile: ProfileUpdateSchema | ProfilePartialUpdateSchema,
    profile_id: UUID,
):
    """Update a profile

    This method is for updating a specific profile
    """
    update_query = (
        update(Profile).where(Profile.id == profile_id).values(**profile.model_dump())
    )
    db.execute(update_query)
    db.commit()
    db_profile = get_profile(db, profile_id)
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: UUID) -> str | NotFoundError:
    """Delete a profile

    This method is for deleting a profile.
    This is a logical deletion, not physical.
    """
    profile = get_profile(db, profile_id)
    if not profile:
        raise NotFoundError("Profile not found")

    profile.is_active = False
    db.commit()
    db.refresh(profile)
    return "Profile deleted successfuly"
