from sqlalchemy import Column, Table, Integer, ForeignKey, UUID
from portaled.database import db


user_institution_table = Table(
    "user_institutions",
    db.Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id")),
    Column("institution_id", Integer, ForeignKey("institutions.id")),
)
