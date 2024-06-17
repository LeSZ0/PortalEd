from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from portaled.schemas.category import (
    CategorySchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
)
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.category as queries
from portaled.auth.utils import verify_token
from typing import Optional


category_apis = APIRouter(
    prefix="/categories", tags=["categories"], dependencies=[Depends(verify_token)]
)


@category_apis.get("", response_model=list[CategorySchema])
def get_documents(
    db: Session = Depends(get_db), getall: Optional[bool] = None
) -> list[CategorySchema]:
    categories = queries.get_categories(db, getall)
    return categories


@category_apis.post("", response_model=CategorySchema, status_code=201)
def create_event(
    category: CategoryCreateSchema, db: Session = Depends(get_db)
) -> CategorySchema:
    db_category = queries.create_category(db=db, category=category)
    return db_category


@category_apis.get(
    "/{category_id}", response_model=CategorySchema, name="Category details"
)
def get_category_by_id(
    category_id: int, db: Session = Depends(get_db)
) -> CategorySchema:
    category = queries.get_category(db=db, category_id=category_id)
    return category


@category_apis.put("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: int, category: CategoryUpdateSchema, db: Session = Depends(get_db)
) -> CategorySchema:
    db_category = queries.update_category(
        db=db, category_id=category_id, category=category
    )
    return db_category


@category_apis.delete("/{category_id}", response_class=JSONResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    msg = queries.delete_category(db=db, category_id=category_id)
    return JSONResponse(msg, status_code=202)
