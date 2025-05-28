from fastapi import Depends
from app.core.dependencies import get_db
from app.core.security import get_current_user

def get_db_dep(db=Depends(get_db)):
    return db

def get_current_user_dep(user=Depends(get_current_user)):
    return user
