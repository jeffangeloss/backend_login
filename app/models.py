import uuid
from sqlalchemy import UUID, Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(
        # es diferente porque el id es de tipo uuid
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()), #lambda es la función anónima de python
        index=True
    )
    username = Column(String, unique=True)
    password = Column(String, unique=True)
    perfil = relationship("Perfil", back_populates="usuario", uselist=False) # Uselist false para que no te devuelva una lista, sino un perfil

class Perfil(Base):
    __tablename__ = "perfil"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(String)
    pais = Column(String)
    usuario_id = Column(
        String(36),
        ForeignKey("usuario.id", unique = True)
    )
    usuario = relationship("Usuario",back_populates="perfil")

class Acceso(Base):
    __tablename__ = "acceso"
    id = Column(
        String,
        primary_key = True,
        index = True
    )
    ultimo_login = Column(
        DateTime
    )
# sqlalchemy se encarga de hacer todas las sentencias sql!
class CategoriaModel(Base):
    __tablename__ = "categoria"
    id = Column(
        # Esto solo funciona para postgres
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    nombre = Column(String)