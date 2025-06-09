from sqlalchemy import Column, Integer, String

from app.db import Base

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

