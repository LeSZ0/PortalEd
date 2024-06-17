from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from uuid import UUID
from portaled.schemas.post import PostCreateSchema, PostSchema, PostUpdateSchema
from portaled.models.post import Post, Tag
from portaled.utils.errors import NotFoundError
from portaled.queries.user import get_user


def get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise NotFoundError("Post not found")

    return post


def get_posts(db: Session, user_id: UUID | None = None) -> list[Post]:
    if user_id:
        # author = get_user(db, user_id)
        return (
            db.query(Post).filter(Post.author.id == user_id).order_by(Post.title).all()
        )

    return db.query(Post).order_by(Post.title).all()


def create_post(db: Session, post: PostCreateSchema, user_id: UUID) -> Post:
    db_post = Post(
        title=post.title,
        slug=post.slug,
        body=post.body,
        author_id=user_id,
        created_at=post.created_at,
        last_update=post.last_update,
    )

    post_tags = []
    for tag in post.tags:
        db_tag = db.query(Tag).filter(Tag.name == tag).first()
        if not db_tag:
            db_tag = Tag(name=tag)
            db.add(db_tag)
            post_tags.append(db_tag)

        else:
            post_tags.append(db_tag)

    db_post.tags = post_tags
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


def update_post(db: Session, post_id: int, post: PostUpdateSchema) -> Post:
    update_query = update(Post).where(Post.id == post_id).values(**post.model_dump())
    db.execute(update_query)
    db.commit()
    db_post = get_post(db, post_id)
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> str:
    delete_query = delete(Post).where(Post.id == post_id)
    db.execute(delete_query)
    db.commit()

    return "Post deleted successfuly"
