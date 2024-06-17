from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models.document import Document
from portaled.schemas.document import DocumentCreateSchema, DocumentUpdateSchema
from portaled.utils.errors import NotFoundError
from typing import Optional


def get_document(db: Session, document_id: UUID) -> Document | NotFoundError:
    """Get a document by id

    Method for quering the database and get a document by id
    """
    document = db.get(Document, document_id)
    if not document:
        raise NotFoundError("Event not found")

    return document


def get_documents(
    db: Session, category: Optional[str] = None, user_id: Optional[UUID] = None
) -> list[Document]:
    """Get a list of documents

    Method for quering the database and get a list of documents.
    """

    main_query = db.query(Document)

    if category:
        main_query.filter(Document.category.like(category))

    if user_id:
        main_query.filter(Document.created_by_id == user_id)

    return main_query.order_by(Document.name).all()


def create_document(
    db: Session, user_id: UUID, document: DocumentCreateSchema
) -> Document:
    """Create a document

    Method for quering the database and creating a new document.
    """
    db_document = Document(
        id=document.id,
        name=document.name,
        slug=document.slug,
        url=document.url,
        category_id=document.category_id,
        created_by_id=user_id,
        created_at=document.created_at,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def update_document(
    db: Session, document_id: UUID, document: DocumentUpdateSchema
) -> Document:
    """Update a document

    This method is for updating a specific document
    """
    update_query = (
        update(Document)
        .where(Document.id == document_id)
        .values(**document.model_dump())
    )
    db.execute(update_query)
    db.commit()
    db_document = get_document(db, document_id)
    db.refresh(db_document)
    return db_document


def delete_document(db: Session, document_id: UUID) -> str | NotFoundError:
    """Delete a document

    This method is for deleting a document.
    """
    if not get_document(db, document_id):
        raise NotFoundError("Document not found")

    delete_query = delete(Document).where(Document.id == document_id)
    db.execute(delete_query)
    db.commit()

    return "Event deleted successfuly"
