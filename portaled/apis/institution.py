from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from portaled.schemas.institution import (
    InstitutionSchema,
    InstitutionCreateSchema,
    InstitutionUpdateSchema,
)
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.institution as queries
from portaled.auth.utils import verify_token
from typing import Optional


institution_apis = APIRouter(prefix="/institutions", tags=["institutions"])


@institution_apis.get("", response_model=list[InstitutionSchema])
def get_institutions(
    db: Session = Depends(get_db),
    name: Optional[str] = None,
    getall: Optional[bool] = None,
) -> list[InstitutionSchema]:
    categories = queries.get_institutions(db, name, getall)
    return categories


@institution_apis.post(
    path="",
    response_model=InstitutionSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_token)],
)
def create_institution(
    institution: InstitutionCreateSchema, db: Session = Depends(get_db)
) -> InstitutionSchema:
    db_institution = queries.create_institution(db=db, institution=institution)
    return db_institution


@institution_apis.get(
    path="/{institution_id}",
    response_model=InstitutionSchema,
    name="Institution details",
    dependencies=[Depends(verify_token)],
)
def get_institution_by_id(
    institution_id: int, db: Session = Depends(get_db), code: Optional[str] = None
) -> InstitutionSchema:
    institution = queries.get_institution(
        db=db, institution_id=institution_id, code=code
    )
    return institution


@institution_apis.put(
    path="/{institution_id}",
    response_model=InstitutionSchema,
    dependencies=[Depends(verify_token)],
)
def update_institution(
    institution_id: int,
    institution_schema: InstitutionUpdateSchema,
    db: Session = Depends(get_db),
) -> InstitutionSchema:
    db_institution = queries.update_institution(
        db=db, institution_id=institution_id, schema=institution_schema
    )
    return db_institution


@institution_apis.delete(
    path="/{institution_id}",
    response_class=JSONResponse,
    dependencies=[Depends(verify_token)],
)
def delete_institution(
    institution_id: int, db: Session = Depends(get_db)
) -> JSONResponse:
    msg = queries.delete_institution(db=db, institution_id=institution_id)
    return JSONResponse(content={'message': msg}, status_code=status.HTTP_200_OK)
