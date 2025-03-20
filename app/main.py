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
    USER_ID = Column(Integer, primary_key=True)
    USERNAME = Column(String(30), unique=True, nullable=False)
    EMAIL = Column(String(30), unique=True, nullable=False)
    PASSWORD = Column(String(50), nullable=False)

class Contacto(Base):
    __tablename__ = "CONTACTO"
    CONTACTO_ID = Column(Integer, primary_key=True)
    USER_ID = Column(Integer, nullable=False)
    LADA_PAIS = Column(Integer, nullable=False)
    LADA_LOCAL = Column(Integer, nullable=False)
    TELEFONO = Column(String(10), nullable=False)
    TIPO_TELEFONO = Column(String(10), nullable=False)
    NUM_EXTERIOR = Column(String(10), nullable=False)
    NUM_INTERIOR = Column(String(10), nullable=False)
    CALLE = Column(String(20), nullable=False)
    COLONIA = Column(String(30), nullable=False)
    CIUDAD = Column(String(20), nullable=False)
    ENTIDAD = Column(String(20), nullable=False)
    PAIS = Column(String(20), nullable=False)
    CODIGO_POSTAL = Column(String(10), nullable=False)
    NOMBRE_S = Column(String(30), nullable=False)
    APELLIDO_S = Column(String(30), unique=True, nullable=False)

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
    USER_ID: int
    USERNAME: str
    EMAIL: str
    PASSWORD: str

# Pydantic model for updating contact info
class UpdateContact(BaseModel):
    CONTACTO_ID : int
    USER_ID : int
    LADA_PAIS : int
    LADA_LOCAL : int
    TELEFONO : str
    TIPO_TELEFONO : str
    NUM_EXTERIOR : str
    NUM_INTERIOR : str
    CALLE : str
    COLONIA : str
    CIUDAD : str
    ENTIDAD : str
    PAIS : str
    CODIGO_POSTAL : str
    NOMBRE_S : str
    APELLIDO_S : str


# Pydantic model for adding data
class GetUser(BaseModel):
    USER_ID : int
    USERNAME : str
    EMAIL: str
    PASSWORD: str


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

# API endpoint to update contacts
@app.post("/updateContact", response_model=GetUser)
async def create_item(contact: UpdateContact, db: Session = Depends(get_db)):
    db_contacto = Contacto(**contact.dict())
    db.add(db_contacto)
    db.commit()
    db.refresh(db_contacto)
    return db_contacto

# API endpoint to read a user by ID
@app.get("/users/{USER_ID}", response_model=GetUser)
async def read_item(USER_ID: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.USER_ID == USER_ID).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)