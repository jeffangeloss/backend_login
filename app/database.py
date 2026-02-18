from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

CADENA_CONEXION = os.getenv("DATABASE_URL")
# Esto realmente es muy inseguro. En un proyecto real, esta cadena de conexión no debería estar hardcodeada, 
# sino que debería estar en una variable de entorno o en un archivo de configuración que no se suba a github
print(CADENA_CONEXION)

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