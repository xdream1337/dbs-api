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


def get_author(db: Session, author: schemas.Optional[AuthorBase] = None, author_id: Optional[UUID4] = None):
    if author is None:
        return db.query(models.Author).filter(models.Author.id == author_id).first()
    return db.query(models.Author).filter(models.Author.id == author.id).first()


def create_author(db: Session, author: schemas.AuthorBase = None ):
    if author.id is None:
        author.id = str(uuid4())
    author_scheme = schemas.AuthorObject(
        **author.dict(), created_at=datetime.now(), updated_at=datetime.now()
    )
    new_author = models.Author(**author_scheme.dict())
    db.add(new_author)
    db.commit()
    return author_scheme

def update_author(db: Session, author: schemas.AuthorBase):
    db_author = db.query(models.Author).filter(models.Author.id == author.id).first()
    for key, value in author.dict(exclude_unset=True).items():
        if value is not author.id:
            setattr(db_author, key, value)
    db_author.updated_at = datetime.now()
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db:Session, author_id: UUID4):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise ValueError(f"Author with ID {author_id} not found")
    db.delete(author)
    db.commit()
    
