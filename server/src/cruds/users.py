from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from src.models import users as user_model
from src.schemas import users as user_schema


def get_users(db: Session):
    return db.query(user_model.User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def register_user(db: Session, user: user_schema.UserBase):
    user_dict = user.dict()
    db_user = user_model.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
def update_user(db: Session, user_id: int, user: user_schema.UserBase):
    user_dict = user.dict()
    db.query(user_model.User).filter(user_model.User.id == user_id).update(user_dict)
    user_dict['id'] = user_id
    db.commit()
    return user_dict

def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()