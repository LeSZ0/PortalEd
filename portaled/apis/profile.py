from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
from portaled.models.profile import Profile
from portaled.database.db import get_db
from portaled.schemas.profile import (
    ProfileSchema,
    ProfileCreateSchema,
    ProfileUpdateSchema,
    ProfilePartialUpdateSchema,
)
import portaled.queries.profile as queries
from portaled.auth.utils import verify_token


profile_apis = APIRouter(
    prefix="/profiles", tags=["profiles"], dependencies=[Depends(verify_token)]
)


@profile_apis.get("", response_model=list[ProfileSchema])
async def get_profiles(db: Session = Depends(get_db)) -> list[ProfileSchema]:
    return queries.get_profiles(db)


@profile_apis.post("", response_model=ProfileSchema)
async def create_profile(
    profile: ProfileCreateSchema,
    db: Session = Depends(get_db),
) -> ProfileSchema:
    db_profile = queries.create_profile(db=db, profile=profile)
    return db_profile


@profile_apis.get("/{profile_id}", response_model=ProfileSchema, name="Get profile")
async def get_profile_by_id(
    profile_id: UUID, db: Session = Depends(get_db)
) -> ProfileSchema:
    profile: Profile = queries.get_profile(db, profile_id)
    return profile


@profile_apis.put("/{profile_id}", response_model=ProfileSchema)
async def update_profile(
    profile_id: UUID, profile: ProfileUpdateSchema, db: Session = Depends(get_db)
) -> ProfileSchema:
    profile: Profile = queries.update_profile(db, profile, profile_id)
    return profile

@profile_apis.patch("/{profile_id}", response_model=ProfileSchema)
async def patch_profile(
    profile_id: UUID, profile: ProfilePartialUpdateSchema, db: Session = Depends(get_db)
) -> ProfileSchema:
    profile: Profile = queries.update_profile(db, profile, profile_id)
    return profile


@profile_apis.delete("/{profile_id}")
async def delete_profile(
    profile_id: UUID, db: Session = Depends(get_db)
) -> JSONResponse:
    queries.delete_profile(db, profile_id)
    return JSONResponse("Profile deleted successfuly", status_code=202)
