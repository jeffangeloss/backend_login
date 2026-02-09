import uuid
from sqlalchemy import Column, String
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