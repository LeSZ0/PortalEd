from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from portaled.schemas import (
    AssignmentSchema,
    AssignmentCreateSchema,
    AssignmentUpdateSchema,
)
from portaled.database.db import DBSession
from sqlalchemy.orm import Session
import portaled.queries.assignment as queries
from portaled.auth.utils import verify_token
from portaled.auth.dependencies import AuthorizatedUser
from typing import Optional
from uuid import UUID
from datetime import datetime


assignments_apis = APIRouter(prefix="/assignments", tags=["assignments"], dependencies=[Depends(verify_token)])


@assignments_apis.get("", response_model=list[AssignmentSchema])
async def get_assignments(db: DBSession, grade_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> list[AssignmentSchema]:
    assignments = queries.get_assignments(db=db, grade_id=grade_id, date_from=date_from, date_to=date_to)
    return assignments


@assignments_apis.post("", response_model=AssignmentSchema, status_code=status.HTTP_201_CREATED)
async def create_assignment(db: DBSession, assignment_schema: AssignmentCreateSchema, user: AuthorizatedUser):
    db_assignment = queries.create_assignment(db, schema=assignment_schema, user_id=user.id)
    return db_assignment


@assignments_apis.get("/{assignment_id}", response_model=AssignmentSchema, status_code=status.HTTP_200_OK, name="Assignment details")
async def get_assignment_by_id(db: DBSession, assignment_id: UUID):
    db_assignment = queries.get_assignment(db, assignment_id)
    return db_assignment


@assignments_apis.put("/{assignment_id}", response_model=AssignmentSchema, status_code=status.HTTP_200_OK)
async def update_assignment(db: DBSession, assignment_id: UUID, assignment_schema: AssignmentUpdateSchema, user: AuthorizatedUser):
    db_assignment = queries.update_assignment(db, assignment_id=assignment_id, schema=assignment_schema, user_id=user.id)
    return db_assignment


@assignments_apis.delete("/{assignment_id}", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def delete_assignment(db: DBSession, assignment_id: UUID, user: AuthorizatedUser):
    msg = queries.delete_assignment(db, assignment_id=assignment_id, user_id=user.id)
    return JSONResponse(
        content={"message": msg},
        status_code=status.HTTP_200_OK
    )
