from main import *
from fastapi import Depends, HTTPException, Body
from sqlalchemy.orm import Session
from src.cruds import books as books_crud
from src.schemas import books as books_schema
from src.database.database import *
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books{user_id}", tags=["books"])
def get_books(user_id: int, db: Session = Depends(get_db)):
    db_books = books_crud.get_books(db=db, user_id=user_id)
    if db_books:
        response = {
            'books_total_count': len(db_books),
            'books': jsonable_encoder(db_books)
            }
        return response

    raise HTTPException(status_code=404, detail="Books not found on this user")
    
@app.post("/book/save/{user_id}", tags=["books"], response_model=books_schema.BookComplete)
def add_book(user_id: int ,book: books_schema.BookBase = Body(..., embed=True), db: Session = Depends(get_db)):
    db_book = books_crud.add_book(db=db, user_id=user_id , book=book)
    if db_book:
        response = {
            'status': 'sucess',
            'book': jsonable_encoder(db_book)
            }
        return JSONResponse(content=response)
    
    raise HTTPException(status_code=404, detail="User does not exist")

@app.delete("/book/delete/{book_id}", tags=["books"], response_model= books_schema.Status)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = books_crud.get_book_by_id(db=db, book_id=book_id)
    if db_book: 
        books_crud.delete_book(db= db, book_id=book_id)
        return books_schema.Status(message="The Book was successfully deleted")
    
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/book/update/{book_id}", tags=["books"], response_model= books_schema.BookBase)
def update_book(book_id: int ,book: books_schema.BookBase = Body(..., embed=True), db: Session = Depends(get_db)):
    db_book = books_crud.get_book_by_id(db=db, book_id=book_id)
    if db_book:
        db_book = books_crud.update_book(db=db, book_id=book_id, book=book)
        response = {
            'status': 'sucess updated',
            'book': jsonable_encoder(db_book)
            }
        return JSONResponse(content=response)
    
    raise HTTPException(status_code=404, detail="Book not found")