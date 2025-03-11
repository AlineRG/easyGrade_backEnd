from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Database setup
DATABASE_URL = "sqlite:///./instance/easyGrade.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = "USER"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

class Contacto(Base):
    __tablename__ = "CONTACTO"
    id = Column(Integer, primary_key=True)
    telefono = Column(String(30), unique=True, nullable=False)
    direccion = Column(String(30), unique=True, nullable=False)
    correo_electronico = Column(String(30), unique=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for adding data
class AddUser(BaseModel):
    username: str
    email: str
    password: str

# Pydantic model for adding data
class GetUser(BaseModel):
    id: int
    username: str
    email: str
    password: str


@app.get("/")
def index():
    return {"data": "Hello world!"}

# API endpoint to create a user
@app.post("/addUser", response_model=GetUser)
async def create_item(user: AddUser, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# API endpoint to read a user by ID
@app.get("/users/{user_id}", response_model=GetUser)
async def read_item(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)