from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.db_models import Contacto

perfilRouter = APIRouter()

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

# API endpoint to update contacts
@perfilRouter.put("/updateContact", response_model=UpdateContact)
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


@perfilRouter.get("/contacto/{user_id}")
def get_contacto_by_user_id(user_id: int, db: Session = Depends(get_db)):
    contacto = db.query(Contacto).filter(Contacto.USER_ID == user_id).first()
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto
