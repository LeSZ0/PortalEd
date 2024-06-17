from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from portaled.schemas.post import PostCreateSchema, PostSchema, PostUpdateSchema
from portaled.database.db import get_db
from sqlalchemy.orm import Session
import portaled.queries.post as queries
from portaled.auth.utils import verify_token
from portaled.auth.dependencies import AuthorizatedUser


post_apis = APIRouter(
    prefix="/posts", tags=["posts"], dependencies=[Depends(verify_token)]
)


@post_apis.get("", response_model=list[PostSchema])
async def get_posts(db: Session = Depends(get_db)) -> list[PostSchema]:
    posts = queries.get_posts(db)
    return posts


@post_apis.post("", response_model=PostSchema)
async def create_post(
    post: PostCreateSchema, user: AuthorizatedUser, db: Session = Depends(get_db)
) -> PostSchema:
    db_post = queries.create_post(db, post, user.id)
    return db_post


@post_apis.get("/{post_id}", response_model=PostSchema)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)) -> PostSchema:
    post = queries.get_post(db, post_id)
    return post


@post_apis.put("/{post_id}", response_model=PostSchema)
async def update_post(
    post_id: int, post: PostUpdateSchema, db: Session = Depends(get_db)
) -> PostSchema:
    db_post = queries.update_post(db, post_id, post)
    return db_post


@post_apis.delete("/{post_id}", response_class=JSONResponse)
async def delete_post(post_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    msg = queries.delete_post(db, post_id)
    return JSONResponse(content=msg, status_code=202)
