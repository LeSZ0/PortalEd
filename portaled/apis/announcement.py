from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from portaled.schemas import (
    AnnouncementCreateSchema,
    AnnouncementUpdateSchema,
    AnnouncementSchema,
)
from portaled.database.db import DBSession
from sqlalchemy.orm import Session
import portaled.queries.announcement as queries
from portaled.auth.utils import verify_token
from portaled.auth.dependencies import AuthorizatedUser
from typing import Optional
from uuid import UUID


announcement_apis = APIRouter(prefix="/announcements", tags=["announcements"], dependencies=[Depends(verify_token)])


@announcement_apis.get("", response_model=list[AnnouncementSchema])
def get_announcements(db: DBSession, institution_id: int, grade_id: Optional[int] = None, user_id: Optional[UUID] = None):
    announcements = queries.get_announcements(db=db, institution_id=institution_id, grade_id=grade_id, user_id=user_id)
    return announcements


@announcement_apis.post("", response_model=AnnouncementSchema, status_code=status.HTTP_201_CREATED)
def create_announcement(db: DBSession, announcement_schema: AnnouncementCreateSchema):
    db_announcement = queries.create_announcement(db=db, schema=announcement_schema)
    return db_announcement


@announcement_apis.get("/{announcement_id}", response_model=AnnouncementSchema, status_code=status.HTTP_200_OK, name="Announcement details")
def get_announcement_by_id(db: DBSession, announcement_id: UUID):
    db_announcement = queries.get_announcement(db, announcement_id)
    return db_announcement


@announcement_apis.put("/{announcement_id}", response_model=AnnouncementSchema, status_code=status.HTTP_200_OK)
def update_announcement(db: DBSession, announcement_id: UUID, announcement_schema: AnnouncementUpdateSchema):
    db_announcement = queries.update_announcement(db, announcement_id=announcement_id, schema=announcement_schema)
    return db_announcement


@announcement_apis.delete("/{announcement_id}", response_class=JSONResponse, status_code=status.HTTP_200_OK)
def delete_announcement(db: DBSession, announcement_id: UUID):
    msg = queries.delete_announcement(db, announcement_id)
    return JSONResponse(
        content={"message": msg},
        status_code=status.HTTP_200_OK
    )
