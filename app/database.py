from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CADENA_CONEXION = "postgresql://videojuegos:videojuegos@localhost:5432/bd_videojuegos"

engine = create_engine(CADENA_CONEXION)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db(): # función dependencia... para esto sirven las dependencias
    # para cada enpoint abre una sesión para la base de datos
    # abre antes de ejecutar el enpoint y cierra la comunicación cuando se finaliza
    db = session()
    try:
        yield db
    finally:
        db.close()