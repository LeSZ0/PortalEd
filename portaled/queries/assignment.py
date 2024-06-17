from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models import Assignment
from portaled.schemas import AssignmentCreateSchema, AssignmentUpdateSchema
from portaled.utils.errors import NotFoundError, AlreadyExistError, UnauthorizedError
from typing import Optional
from datetime import datetime


def get_assignments(db: Session, grade_id: int, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> list[Assignment]:
    db_assignments = db.query(Assignment).filter(Assignment.grade_id == grade_id)
    if date_from:
        db_assignments.filter(Assignment.created_at >= date_from)

    if date_to:
        db_assignments.filter(Assignment.created_at <= date_to)

    return db_assignments.order_by(Assignment.created_at).all()


def get_assignment(db: Session, assignment_id: UUID) -> Assignment:
    db_assignment = db.get(Assignment, assignment_id)
    if not db_assignment:
        raise NotFoundError("Assignment not found")

    return db_assignment


def create_assignment(db: Session, schema: AssignmentCreateSchema, user_id: UUID) -> Assignment:
    if db.query(Assignment).filter(Assignment.identifier == schema.identifier).first():
        raise AlreadyExistError(f"The assignment with identifier {schema.identifier} already exist")

    db_assignment = Assignment(**schema.model_dump())
    db_assignment.crated_by_id = user_id
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    return db_assignment


def update_assignment(db: Session, assignment_id: UUID, schema: AssignmentUpdateSchema, user_id: UUID) -> Assignment:
    db_assignment = get_assignment(db, assignment_id)

    if not db_assignment.crated_by_id == user_id:
        raise UnauthorizedError("You don't haver permissions to perform this operation")

    update_query = (
        update(Assignment)
        .where(Assignment.id == assignment_id)
        .values(**schema.model_dump(exclude_none=True))
    )
    db.execute(update_query)
    db.commit()
    db.refresh(db_assignment)

    return db_assignment


def delete_assignment(db: Session, assignment_id: UUID, user_id: UUID):
    db_assignment = get_assignment(db, assignment_id)

    if not db_assignment.crated_by_id == user_id:
        raise UnauthorizedError("You don't haver permissions to perform this operation")
    
    delete_query = delete(Assignment).where(Assignment.id == assignment_id)
    db.execute(delete_query)
    db.commit()

    return "Assignment deleted successfuly"
