from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from . import models, schemas
from datetime import datetime
from uuid import uuid4
from pydantic import UUID4


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def get_author(db: Session, author: schemas.AuthorBase):
    return db.query(models.Author).filter(models.Author.id == author.id).first()


def create_author(db: Session, author: schemas.AuthorBase):
    if author.id is None:
        author.id = str(uuid4())
    author_scheme = schemas.AuthorObject(
        **author.dict(), created_at=datetime.now(), updated_at=datetime.now()
    )
    new_author = models.Author(**author_scheme.dict())
    db.add(new_author)
    db.commit()
    return author_scheme


def get_category(db: Session, category: schemas.CategoryBase):
    category_id = (
        db.query(models.Category).filter(models.Category.id == category.id).first()
    )
    category_name = (
        db.query(models.Category).filter(models.Category.name == category.name).first()
    )

    if category_id:
        return category_id
    elif category_name:
        return category_name
    else:
        return None


def create_category(db: Session, category: schemas.CategoryBase):
    if category.id is None:
        category.id = str(uuid4())
    category_scheme = schemas.CategoryObject(
        **category.dict(), created_at=datetime.now(), updated_at=datetime.now()
    )
    new_category = models.Category(**category_scheme.dict())
    db.add(new_category)
    db.commit()
    return category_scheme
