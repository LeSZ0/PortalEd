from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from portaled.schemas.comment import (
    CommentSchema,
    CommentCreateSchema,
    CommentUpdateSchema,
)
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.comment as queries
from portaled.auth.utils import verify_token
from portaled.auth.dependencies import AuthorizatedUser


comment_apis = APIRouter(
    prefix="/comments", tags=["comments"], dependencies=[Depends(verify_token)]
)


@comment_apis.get("", response_model=list[CommentSchema])
def get_comments(post_id: int, db: Session = Depends(get_db)) -> list[CommentSchema]:
    comments = queries.get_comments(post_id=post_id, db=db)
    return comments


@comment_apis.post("", response_model=CommentSchema)
def add_comment_to_post(
    comment: CommentCreateSchema, user: AuthorizatedUser, db: Session = Depends(get_db)
) -> CommentSchema:
    comment = queries.create_comment(db=db, user_id=user.id, comment=comment)
    return comment


@comment_apis.get("/{comment_id}", response_model=CommentSchema)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)) -> CommentSchema:
    comment = queries.get_comment(db=db, comment_id=comment_id)
    return comment


@comment_apis.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment: CommentUpdateSchema,
    user: AuthorizatedUser,
    db: Session = Depends(get_db),
) -> CommentSchema:
    comment = queries.update_comment(
        db=db, comment_id=comment_id, comment=comment, user_id=user.id
    )
    return comment


@comment_apis.delete("/{comment_id}", response_class=JSONResponse)
def delete_comment(
    comment_id: int, user: AuthorizatedUser, db: Session = Depends(get_db)
) -> JSONResponse:
    msg = queries.delete_comment(db, comment_id, user)
    return JSONResponse(content=msg, status_code=202)
