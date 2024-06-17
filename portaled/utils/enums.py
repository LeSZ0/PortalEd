from enum import StrEnum


class Role(StrEnum):
    TEACHER = "teacher"
    STUDENT = "student"
    MANAGEMENT = "management"


class Statuses(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    IN_REVISION = "in_revision"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    DONE = "done"
