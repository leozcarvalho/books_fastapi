from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from src.models import books as books_model
from src.cruds import users as users_model
from src.schemas import books as books_schema

def get_books(db: Session, user_id: int):
    return db.query(books_model.Books).filter(books_model.Books.owner_user == user_id).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(books_model.Books).filter(books_model.Books.id == book_id).first()

def add_book(db: Session, user_id: int, book: books_schema.BookBase):
    db_user = users_model.get_user_by_id(db=db, user_id=user_id)
    if db_user:
        book_dict = book.dict()
        book_dict['owner_user'] = user_id
        db_book = books_model.Books(**book_dict)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db=db, book_id=book_id)
    db.delete(db_book)
    db.commit()

def update_book(db: Session, book_id: int, book: books_schema.BookBase):
    book_dict = book.dict()
    db.query(books_model.Books).filter(books_model.Books.id == book_id).update(book_dict)
    book_dict['id'] = book_id
    db.commit()
    return book_dict