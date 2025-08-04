from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel

from app.db import get_db
from app.db_models import Materia, RegistroMateriasUsuario

materiasRouter = APIRouter()

# Pydantic models for validating input data
class MateriaUpdate(BaseModel):
    NOMBRE: str
    NIVEL: str


class UpdateRegistroMateriasUsuario(BaseModel):
    USER_ID: int
    MATERIA_ID: int


class MateriaCreate(BaseModel):
    NOMBRE: str
    NIVEL: str


# FastAPI pueda convertir el modelo de SQLAlchemy a Pydantic automáticamente.
# return db_materia está devolviendo un objeto SQLAlchemy
# con orm_mode = True, FastAPI puede convertirlo automáticamente al JSON
class MateriaOut(BaseModel):
    MATERIA_ID: int
    NOMBRE: str
    NIVEL: str

    class Config:
        orm_mode = True

@materiasRouter.get("/todasMaterias", response_model=list[MateriaOut])
def get_all_materias(db: Session = Depends(get_db)):
    materias = db.query(Materia).all()
    return materias

@materiasRouter.get("/materias/{user_id}", response_model=list[MateriaOut])
def get_materias(user_id: int, db: Session = Depends(get_db)):
    materias = db.query(Materia).filter(Materia.USER_ID == user_id).all()
    return materias


@materiasRouter.post("/agregarMateria", response_model=MateriaOut)
def agregar_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    existing = db.query(Materia).filter(
        and_(Materia.NOMBRE == materia.NOMBRE, Materia.NIVEL == materia.NIVEL)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Esa NOMBRE de materia con ese NIVEL ya se encuentran en la base de datos.")
    
    db_materia = Materia(**materia.dict())
    db.add(db_materia)
    db.commit()
    db.refresh(db_materia)
    return db_materia


@materiasRouter.put("/editarMateria/{materia_id}", response_model=MateriaOut)
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
@materiasRouter.post(
    "/updateRegistroMateriasUsuario", response_model=UpdateRegistroMateriasUsuario
)
async def create_item(
    register: UpdateRegistroMateriasUsuario, db: Session = Depends(get_db)
):
    db_register = RegistroMateriasUsuario(**register.dict())
    db.add(db_register)
    db.commit()
    db.refresh(db_register)
    return db_register


@materiasRouter.get("/getMateriasByUserID")
def get_materias_by_user_id(user_id: int, db: Session = Depends(get_db)):
    materia_ids = (
        db.query(RegistroMateriasUsuario)
        .filter(RegistroMateriasUsuario.USER_ID == user_id)
        .all()
    )
    if not materia_ids:
        raise HTTPException(
            status_code=404, detail="No se encontraron materias para el usuario"
        )

    materia_ids = [register.MATERIA_ID for register in materia_ids]

    materias = (
        db.query(Materia.MATERIA_ID, Materia.NOMBRE, Materia.NIVEL)
        .filter(Materia.MATERIA_ID.in_(materia_ids))
        .all()
    )
    materias = [materia._mapping for materia in materias]
    return materias
