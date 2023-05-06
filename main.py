from fastapi import FastAPI, HTTPException, Depends
from . import crud, schemas, database, models
from sqlalchemy.orm import Session
from typing import List
import uuid


app = FastAPI()


@app.on_event("startup")
def startup():
    with database.SessionLocal() as session:
        # Create tables if they do not exist
        models.Base.metadata.create_all(bind=database.engine)
    print("Database created")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user_id, user)


@app.post("/authors", response_model=schemas.AuthorObject)
def new_author(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    if author.id is not None:
        try:
            print(author.id)
            val = uuid.UUID(str(author.id), version=4)
        except ValueError:
            raise HTTPException(status_code=400, detail="UUID is not valid")
    db_author = crud.get_author(db, author)
    if db_author is not None:
        raise HTTPException(status_code=400, detail="Author already exists")
    return crud.create_author(db, author)


@app.post("/categories", response_model=schemas.CategoryObject)
def new_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    if category.id is not None:
        try:
            print(category.id)
            val = uuid.UUID(str(category.id), version=4)
        except ValueError:
            raise HTTPException(status_code=400, detail="UUID is not valid")
    db_category = crud.get_category(db, category)
    if db_category is not None:
        raise HTTPException(status_code=409, detail="Category already exists")
    return crud.create_category(db, category)
