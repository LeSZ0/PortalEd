from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models import Announcement
from portaled.schemas import AnnouncementCreateSchema, AnnouncementUpdateSchema
from portaled.utils.errors import NotFoundError
from typing import Optional


def get_announcement(db: Session, announcement_id: UUID) -> Announcement:
    db_announcement = db.get(Announcement, announcement_id)
    if not db_announcement:
        raise NotFoundError("Announcement not found")
    
    return db_announcement


def get_announcements(db: Session, institution_id: int, grade_id: Optional[int] = None, user_id: Optional[UUID] = None) -> list[Announcement]:
    db_announcements = db.query(Announcement).filter(Announcement.institution_id == institution_id)
    if grade_id:
        db_announcements.filter(Announcement.grade_id == grade_id)

    if user_id:
        db_announcements.filter(Announcement.created_by_id == user_id)

    return db_announcements.order_by(Announcement.created_at).all()


def create_announcement(db: Session, schema: AnnouncementCreateSchema) -> Announcement:
    db_announcement = Announcement(**schema.model_dump())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)

    return db_announcement


def update_announcement(db: Session, announcement_id: UUID, schema: AnnouncementUpdateSchema) -> Announcement:
    update_query = (
        update(Announcement)
        .where(Announcement.id == announcement_id)
        .values(**schema.model_dump(exclude_none=True))
    )
    db.execute(update_query)
    db.commit()
    db_announcement = get_announcement(db=db, announcement_id=announcement_id)
    db.refresh(db_announcement)
    return db_announcement


def delete_announcement(db: Session, announcement_id: UUID) -> Announcement:
    delete_query = delete(Announcement).where(Announcement.id == announcement_id)
    db.execute(delete_query)
    db.commit()

    return "Announcement deleted successfuly"
