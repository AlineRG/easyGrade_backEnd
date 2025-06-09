from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import Body

from app.db import get_db
from app.db_models import User

loginRouter = APIRouter()

# Pydantic model for adding data
class AddUser(BaseModel):
    USERNAME: str
    EMAIL: str
    PASSWORD: str

# Pydantic model for adding data
class GetUser(BaseModel):
    USER_ID: int
    USERNAME: str
    EMAIL: str
    PASSWORD: str


# API endpoint to create a user
@loginRouter.post("/addUser", response_model=AddUser)
async def create_item(user: AddUser, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@loginRouter.post("/login")
def login(
    email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.EMAIL == email, User.PASSWORD == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return {
        "USER_ID": user.USER_ID,
        "USERNAME": user.USERNAME,
        "EMAIL": user.EMAIL,
        "PASSWORD": user.PASSWORD,
    }


# API endpoint to read a user by ID
@loginRouter.get("/users/{USER_ID}", response_model=GetUser)
async def read_item(USER_ID: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.USER_ID == USER_ID).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
