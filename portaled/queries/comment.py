from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models.comment import Comment
from portaled.schemas.comment import CommentCreateSchema, CommentUpdateSchema
from portaled.schemas.user import UserSchema
from portaled.queries.post import get_post
from portaled.utils.errors import NotFoundError, UnauthorizedError
from portaled.utils.enums import Role


def get_comment(db: Session, comment_id: int) -> Comment | None:
    """Get a comment by id

    Method for quering the database and get a comment by id
    """
    comment = db.get(Comment, comment_id)
    if not comment:
        raise NotFoundError("Comment not found")

    return comment


def get_comments(db: Session, post_id: int) -> list[Comment]:
    """Get a list of comments

    Method for quering the database and get a list of comments.
    """

    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.updated_at)
    )


def create_comment(db: Session, user_id: UUID, comment: CommentCreateSchema) -> Comment:
    """Add a comment to a post

    Method for quering the database and add a new comment to the post.
    """
    if get_post(db, comment.post_id):
        db_comment = Comment(
            message=comment.message,
            post_id=comment.post_id,
            author_id=user_id,
            updated_at=comment.updated_at,
            creation_at=comment.created_at,
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)

        return db_comment


def update_comment(
    db: Session, comment_id: int, comment: CommentUpdateSchema, user_id: UUID
) -> Comment:
    """Update a comment

    This method is for updating a specific comment.
    Only the creator of the comment can update it.
    """
    db_comment = get_comment(db, comment_id)
    if db_comment.author_id != user_id:
        raise UnauthorizedError("You are not allowed to perform this operation")

    update_query = (
        update(Comment)
        .where(Comment.id == comment_id)
        .where(Comment.author_id == user_id)
        .values(**comment.model_dump())
    )
    db.execute(update_query)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int, user: UserSchema) -> str:
    """Delete a comment

    This method is for deleting a specific comment.
    Only the creator of the comment or a teacher profile can delete it.
    """
    comment = get_comment(db, comment_id)

    if comment.author_id != user.id or user.profile.role != Role.TEACHER:
        raise UnauthorizedError("You are not allowed to perform this operation")

    delete_query = delete(Comment).where(Comment.id == comment_id)
    db.execute(delete_query)
    db.commit()

    return "Comment deleted successfuly"
