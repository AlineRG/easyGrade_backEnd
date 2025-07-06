from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from typing import Optional
import pandas as pd


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "sqlite:///./instance/easyGrade.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = "USER"
    USER_ID = Column(Integer, primary_key=True, autoincrement=True)
    USERNAME = Column(String(30), unique=True, nullable=False)
    EMAIL = Column(String(30), unique=True, nullable=False)
    PASSWORD = Column(String(50), nullable=False)


class Contacto(Base):
    __tablename__ = "CONTACTO"
    CONTACTO_ID = Column(Integer, primary_key=True, autoincrement=True)
    USER_ID = Column(Integer, unique=True, nullable=False)
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
    APELLIDO_S = Column(String(30), nullable=False)


class Materia(Base):
    __tablename__ = "MATERIAS"
    MATERIA_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    NOMBRE = Column(String(100), nullable=False)
    NIVEL = Column(String(50), nullable=False)


class RegistroMateriasUsuario(Base):
    __tablename__ = "REGISTRO_MATERIAS_USER"
    ID = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    USER_ID = Column(Integer,nullable=False)
    MATERIA_ID = Column(Integer,nullable=False)

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
    USERNAME: str
    EMAIL: str
    PASSWORD: str


class UpdateUser(BaseModel):
    USER_ID: int
    USERNAME: str
    EMAIL: str
    PASSWORD: str


# Pydantic model for updating contact info
class UpdateContact(BaseModel):
    USER_ID: int
    LADA_PAIS: int
    LADA_LOCAL: int
    TELEFONO: str
    TIPO_TELEFONO: str
    NUM_EXTERIOR: str
    NUM_INTERIOR: str
    CALLE: str
    COLONIA: str
    CIUDAD: str
    ENTIDAD: str
    PAIS: str
    CODIGO_POSTAL: str
    NOMBRE_S: str
    APELLIDO_S: str


# Pydantic model for adding data
class GetUser(BaseModel):
    USER_ID: int
    USERNAME: str
    EMAIL: str
    PASSWORD: str


class MateriaUpdate(BaseModel):
    NOMBRE: str
    NIVEL: str


class UpdateRegistroMateriasUsuario(BaseModel):
    USER_ID: int
    MATERIA_ID: int

@app.get("/")
def index():
    return {"data": "Hello world!"}


# API endpoint to create a user
@app.post("/addUser", response_model=AddUser)
async def create_item(user: AddUser, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# API endpoint to update contacts
@app.put("/updateContact", response_model=UpdateContact)
async def create_item(contact: UpdateContact, db: Session = Depends(get_db)):
    user_id = contact.USER_ID
    db_user = db.query(Contacto).filter(Contacto.USER_ID == user_id).first()

    if not db_user:  # Contact information has never been added
        db_contacto = Contacto(**contact.dict())
        db.add(db_contacto)
        db.commit()
        db.refresh(db_contacto)
        return db_contacto
    elif db_user:  # USER_ID is found in Contacto
        for field, value in contact.dict().items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user


class MateriaCreate(BaseModel):
    NOMBRE: str
    NIVEL: str


class MateriaOut(BaseModel):
    NOMBRE: str
    NIVEL: str


# API endpoint to read a user by ID
@app.get("/users/{USER_ID}", response_model=GetUser)
async def read_item(USER_ID: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.USER_ID == USER_ID).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/login")
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


@app.put("/updateUser")
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


@app.get("/contacto/{user_id}")
def get_contacto_by_user_id(user_id: int, db: Session = Depends(get_db)):
    contacto = db.query(Contacto).filter(Contacto.USER_ID == user_id).first()
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto


@app.get("/materias/{user_id}", response_model=list[MateriaOut])
def get_materias(user_id: int, db: Session = Depends(get_db)):
    materias = db.query(Materia).filter(Materia.USER_ID == user_id).all()
    return materias


@app.post("/agregarMateria", response_model=MateriaOut)
def agregar_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    db_materia = Materia(**materia.dict())
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia


@app.put("/editarMateria/{materia_id}", response_model=MateriaOut)
def editar_materia(
    materia_id: int, materia: MateriaUpdate, db: Session = Depends(get_db)
):
    db_materia = db.query(Materia).filter(Materia.MATERIA_ID == materia_id).first()
    if not db_materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    db_materia.NOMBRE = materia.NOMBRE
    db_materia.NIVEL = materia.NIVEL

    db.commit()
    db.refresh(db_materia)

    return db_materia

# API endpoint to update REGISTRO_MATERIAS_USUARIO
@app.post("/updateRegistroMateriasUsuario", response_model=UpdateRegistroMateriasUsuario)
async def create_item(register: UpdateRegistroMateriasUsuario, db: Session = Depends(get_db)):
    db_register = RegistroMateriasUsuario(**register.dict())
    db.add(db_register)
    db.commit()
    db.refresh(db_register)
    return db_register


@app.get("/getMateriasByUserID")
def get_materias_by_user_id(user_id:int, db: Session = Depends(get_db)):
    materia_ids = db.query(RegistroMateriasUsuario).filter(RegistroMateriasUsuario.USER_ID == user_id).all()
    if not materia_ids:
        raise HTTPException(status_code=404, detail="No se encontraron materias para el usuario")
    
    materia_ids = [register.MATERIA_ID for register in materia_ids]

    materias = db.query(Materia.MATERIA_ID, Materia.NOMBRE, Materia.NIVEL).filter(Materia.MATERIA_ID.in_(materia_ids)).all()
    materias = [materia._mapping for materia in materias]
    return materias

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
