from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import delete, update
from portaled.models.category import Category
from portaled.schemas.category import CategoryCreateSchema, CategoryUpdateSchema
from portaled.utils.errors import NotFoundError
from typing import Optional


def get_category(
    db: Session, category_id: Optional[int] = None, slug: Optional[str] = None
) -> Category | NotFoundError:
    """Get a category by id

    Method for quering the database and get a category by id or slug
    """
    if not slug and not category_id:
        return

    if slug:
        category = db.query(Category).filter(Category.slug == slug).first()
    else:
        category = db.get(Category, category_id)

    if not category:
        raise NotFoundError("Event not found")

    return category


def get_categories(db: Session, getall: bool = False) -> list[Category]:
    """Get a list of documents

    Method for quering the database and get a list of documents.
    """

    main_query = db.query(Category)

    if not getall:
        main_query.filter(Category.is_active == True)

    return main_query.order_by(Category.name).all()


def create_category(db: Session, category: CategoryCreateSchema) -> Category:
    """Create a category

    Method for quering the database and creating a new category.
    """
    try:
        db_category = get_category(db=db, slug=category.slug)
        db_category.is_active = True
    except NotFoundError:
        db_category = Category(
            name=category.name,
            slug=category.slug,
            created_at=category.created_at,
            updated_at=category.updated_at,
            is_active=category.is_active,
        )
        db.add(db_category)

    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, category_id: int, category: CategoryUpdateSchema
) -> Category:
    """Update a category

    This method is for updating a specific category
    """
    update_query = (
        update(Category)
        .where(Category.id == category_id)
        .values(**category.model_dump())
    )
    db.execute(update_query)
    db.commit()
    db_category = get_category(db=db, category_id=category_id)
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> str | NotFoundError:
    """Delete a category

    This method is for deleting a category.
    This is a logical deletion, not phisical.
    It means that the is_active field will be False, and it can be activated later.
    """
    category = get_category(db=db, category_id=category_id)
    if not category:
        raise NotFoundError("Category not found")

    category.is_active = False
    db.commit()
    db.refresh(category)

    return "Category deleted successfuly"
