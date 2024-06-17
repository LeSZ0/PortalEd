from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models.institution import Institution
from portaled.schemas.institution import InstitutionCreateSchema, InstitutionUpdateSchema
from portaled.utils.errors import NotFoundError
from typing import Optional
from portaled.utils.enums import Role


def get_institutions(
    db: Session, name: Optional[str] = None, getall: bool = False
) -> list[Institution]:
    institutions = db.query(Institution)
    if name:
        institutions.filter(Institution.name.like(f"%{name}%"))

    if not getall:
        institutions.filter(Institution.is_active == True)

    return institutions.order_by(Institution.name, Institution.short_name).all()


def get_institution(
    db: Session, code: Optional[str] = None, institution_id: Optional[int] = None
) -> Institution | NotFoundError:
    if not code and not institution_id:
        return

    if code:
        institution = db.query(Institution).filter(Institution.code == code).first()
    else:
        institution = db.get(Institution, institution_id)

    if not institution:
        raise NotFoundError("Institution not found")

    return institution


def create_institution(
    db: Session, institution: InstitutionCreateSchema
) -> Institution:
    db_institution = Institution(**institution.model_dump())
    db_institution.code = institution.code
    db_institution.is_active = institution.is_active
    db.add(db_institution)
    db.commit()
    db.refresh(db_institution)

    return db_institution


def update_institution(db: Session, institution_id: int, schema: InstitutionUpdateSchema) -> Institution:
    update_query = (
        update(Institution).where(Institution.id == institution_id).values(**schema.model_dump(exclude_none=True))
    )
    db.execute(update_query)
    db.commit()
    db_institution = get_institution(db, institution_id=institution_id)
    db.refresh(db_institution)
    return db_institution


def delete_institution(db: Session, institution_id: int) -> str | NotFoundError:
    """Delete an institution

    This method is for deleting an institution.
    This is a logical deletion, not phisical.
    """
    db_institution = get_institution(db, institution_id=institution_id)
    if not db_institution:
        raise NotFoundError("Institution not found")

    db_institution.is_active = False
    db.commit()
    db.refresh(db_institution)
    return "Institution deleted successfuly"
