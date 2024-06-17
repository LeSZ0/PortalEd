from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from portaled.schemas.document import (
    DocumentSchema,
    DocumentCreateSchema,
    DocumentUpdateSchema,
)
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.document as queries
from portaled.auth.utils import verify_token
from portaled.auth.dependencies import AuthorizatedUser
from uuid import UUID
from typing import Optional


document_apis = APIRouter(
    prefix="/documents", tags=["documents"], dependencies=[Depends(verify_token)]
)


@document_apis.get("", response_model=list[DocumentSchema])
def get_documents(
    user_id: Optional[UUID] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[DocumentSchema]:
    params = {"db": db}

    if user_id:
        params.update({"user_id": user_id})

    if category:
        params.update({"category": category})

    documents = queries.get_documents(**params)
    return documents


@document_apis.post("", response_model=DocumentSchema, status_code=201)
def create_document(
    user: AuthorizatedUser,
    document: DocumentCreateSchema,
    db: Session = Depends(get_db),
) -> DocumentSchema:
    db_document = queries.create_document(db=db, user_id=user.id, document=document)
    return db_document


@document_apis.get(
    "/{document_id}", response_model=DocumentSchema, name="Document details"
)
def get_document_by_id(
    document_id: UUID, db: Session = Depends(get_db)
) -> DocumentSchema:
    document = queries.get_document(db=db, document_id=document_id)
    return document


@document_apis.put("/{document_id}", response_model=DocumentSchema)
def update_document(
    document_id: UUID, document: DocumentUpdateSchema, db: Session = Depends(get_db)
) -> DocumentSchema:
    db_document = queries.update_document(
        db=db, document_id=document_id, document=document
    )
    return db_document


@document_apis.delete("/{document_id}", response_class=JSONResponse)
def delete_document(document_id: UUID, db: Session = Depends(get_db)) -> JSONResponse:
    msg = queries.delete_document(db=db, document_id=document_id)
    return JSONResponse(msg, status_code=202)
