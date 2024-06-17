from sqlalchemy import Column, Table, Integer, ForeignKey, UUID
from portaled.database import db


profile_grade_table = Table(
    "profile_grades",
    db.Base.metadata,
    Column("profile_id", UUID, ForeignKey("profiles.id")),
    Column("grade_id", Integer, ForeignKey("grades.id")),
)
