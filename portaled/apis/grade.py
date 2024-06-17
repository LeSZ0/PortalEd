from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from portaled.schemas.grade import (
    GradeSchema,
    GradeCreateSchema,
    GradeUpdateSchema,
)
from portaled.database.db import DBSession
from sqlalchemy.orm import Session
import portaled.queries.grade as queries
from portaled.auth.utils import verify_token
from typing import Optional


grade_apis = APIRouter(prefix="/grades", tags=["grades"], dependencies=[Depends(verify_token)])


@grade_apis.get("", response_model=list[GradeSchema])
def get_grades(institution_id: int, db: DBSession, getall: Optional[bool] = None) -> list[GradeSchema]:
    assert institution_id, "Institution not defined"

    db_grades = queries.get_grades(db, institution_id=institution_id, getall=getall)
    return db_grades


@grade_apis.post("", response_model=GradeSchema, status_code=status.HTTP_201_CREATED)
def get_grades(grade_schema: GradeCreateSchema, institution_id: int, db: DBSession) -> GradeSchema:
    assert institution_id, "Institution not defined"

    db_grades = queries.create_grade(db, schema=grade_schema, institution_id=institution_id)
    return db_grades


@grade_apis.get("/{grade_id}", response_model=GradeSchema, status_code=status.HTTP_200_OK, name="Grade details")
def get_grade_by_id(grade_id: int, db: DBSession) -> GradeSchema:
    db_grade = queries.get_grade(db, grade_id=grade_id)
    return db_grade


@grade_apis.put("/{grade_id}", response_model=GradeSchema)
def update_grade(grade_id: int, db: DBSession) -> GradeSchema:
    db_grade = queries.update_grade(db=db, grade_id=grade_id)
    return db_grade


@grade_apis.delete("/{grade_id}", response_class=JSONResponse, status_code=status.HTTP_200_OK)
def delete_grade(grade_id: int, db: DBSession) -> JSONResponse:
    msg = queries.delete_grade(db, grade_id)
    return JSONResponse(
        content={"message": msg},
        status_code=status.HTTP_200_OK
    )
