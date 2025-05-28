from sqlalchemy.orm import Session
from app.models.user_model import User as UserModel
from app.schemas.user import UserCreate

def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def create_user(db: Session, user: UserCreate):
    fake_hashed = user.password + "notreallyhashed"
    db_user = UserModel(username=user.username, hashed_password=fake_hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
