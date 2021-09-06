from main import *
from fastapi import Depends, HTTPException, Body
from sqlalchemy.orm import Session
from src.models import users as user_model
from src.cruds import users as user_crud
from src.schemas import users as user_schemas
from src.database.database import *
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", tags=["users"])
def get_user(db: Session = Depends(get_db)):
    db_users = user_crud.get_users(db=db)
    response = {
        'users_total_count': len(db_users),
        'users': jsonable_encoder(db_users)
        }
    return JSONResponse(content=response)

@app.post("/user/register", tags=["users"], response_model=user_schemas.UserBase)
def register_user(user: user_schemas.UserBase = Body(..., embed=True), db: Session = Depends(get_db)):
    db_user = user_crud.register_user(db=db, user=user)
    return db_user