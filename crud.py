from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from . import models, schemas
from datetime import datetime
from uuid import uuid4
from pydantic import UUID4
from typing import Optional, List


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


def create_author(db: Session, author: schemas.AuthorBase = None , author_id: Optional[UUID4] = None):
    if author and author_id is None:
        return None
    if author.id is None:
        author.id = str(uuid4())
    author_scheme = schemas.AuthorObject(
        **author.dict(), created_at=datetime.now(), updated_at=datetime.now()
    )
    new_author = models.Author(**author_scheme.dict())
    db.add(new_author)
    db.commit()
    return author_scheme
