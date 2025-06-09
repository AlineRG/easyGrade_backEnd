from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.db_models import User

privacidadRouter = APIRouter()

# Pydantic model for updating user info
class UpdateUser(BaseModel):
    USER_ID: int
    USERNAME: str
    EMAIL: str
    PASSWORD: str


@privacidadRouter.put("/updateUser")
def update_user(user: UpdateUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.USER_ID == user.USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_user.USER_ID = user.USER_ID
    db_user.USERNAME = user.USERNAME
    db_user.EMAIL = user.EMAIL
    db_user.PASSWORD = user.PASSWORD

    db.commit()
    db.refresh(db_user)

    return {
        "USER_ID": db_user.USER_ID,
        "USERNAME": db_user.USERNAME,
        "EMAIL": db_user.EMAIL,
        "PASSWORD": db_user.PASSWORD,
    }

