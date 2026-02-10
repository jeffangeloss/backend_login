import uuid
from sqlalchemy import UUID, Column, DateTime, String
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