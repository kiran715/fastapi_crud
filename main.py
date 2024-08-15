from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=book.author_id)
    if db_author is None:
        raise HTTPException(status_code=400, detail="Author not found")
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

# curl -X POST "http://127.0.0.1:8000/books/" -H "Content-Type: application/json" -d "{\"title\": \"Art of Programming\", \"author_id\": 3}
# curl "http://127.0.0.1:8000/authors/"

# curl "http://127.0.0.1:8000/books/"

# curl -X POST "http://127.0.0.1:8000/authors/" -H "Content-Type: application/json" -d "{\"name\": \"Kiran\"}"


