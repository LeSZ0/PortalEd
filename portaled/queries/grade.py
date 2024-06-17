from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models.grade import Grade
from portaled.schemas.grade import GradeCreateSchema, GradeUpdateSchema
from portaled.utils.errors import NotFoundError, AlreadyExistError
from typing import Optional
from portaled.utils.enums import Role


def get_grades(db: Session, institution_id: int, getall: bool = False) -> list[Grade]:
    return db.query(Grade).filter(Grade.institution_id == institution_id).order_by(Grade.name).all()


def get_grade(db: Session, grade_id: int) -> Grade:
    grade = db.get(Grade, grade_id)

    if not grade:
        raise NotFoundError("Grade not found")

    return grade


def create_grade(db: Session, schema: GradeCreateSchema) -> Grade:
    if db.query(Grade).filter(Grade.institution_id == schema.institution_id).filter(Grade.name == schema.name).first():
        raise AlreadyExistError(f"The grade {schema.name} already exists")
    
    db_grade = Grade(**schema.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)

    return db_grade


def update_grade(db: Session, grade_id: int, schema: GradeUpdateSchema) -> Grade:
    update_query = (
        update(Grade).where(Grade.id == grade_id).values(**schema.model_dump(exclude_none=True))
    )
    db.execute(update_query)
    db.commit()
    db_grade = get_grade(db, grade_id=grade_id)
    db.refresh(db_grade)
    return db_grade


def delete_grade(db: Session, grade_id: int) -> Grade:
    """Delete a grade

    This method is for deleting a institution grade.
    This is a logical deletion, not phisical.
    """
    db_grade = get_grade(db, grade_id=grade_id)

    db_grade.is_active = False
    db.commit()
    db.refresh(db_grade)
    return "Grade deleted successfuly"
