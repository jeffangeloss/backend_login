import datetime
import time
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .routers import categorias, videojuegos
from .data import accesos
from .database import get_db
from sqlalchemy.orm import Session
from .models import Acceso, Usuario

app = FastAPI()

# Esto es inseguro, pero lo hacemos por ahora
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)
class LoginRequest(BaseModel):
    username : str = Field(..., min_length=5)
    password : str = Field(..., min_length=8)

@app.post("/login")
async def login(login_request : LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        # Modelo usuario usado para hacerle Query's
            # Objeto db es una conexión con la base de datos
            # Una consulta a la tabla usuario y quiero que los resultados los filtres por
        Usuario.username == login_request.username,
        #  los username de usuario que sea igual al username del login_request
        Usuario.password == login_request.password
        #  los password de usuario que sea igual al password del login_request
    ).first()
    
    # En el caso que no exista el usuario con dicho username y ese password
    if not usuario:
        raise HTTPException(
            status_code=400, 
            detail="Error en el login, credenciales incorrectas")
        # return{
        #     "msg" : "Error en login"
        # }
        
    ## Si todo es correcto creamos el token!!!
    # usaremos una librería que se encarge de encriptar
    # bcrypt    
    hora_actual = time.time_ns()
    # time_ns: nano segundos (int)
    cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
    # interpolación de strings, entre llaves se incrustan
    cadena_hasheada = bcrypt.hashpw(
        cadena_a_encriptar.encode("utf-8"),
        bcrypt.gensalt()
    )
    
    # Creamos el objeto en bd → todavía no lo hemos guardado
    # Objeto que se va a guardad en la bd
    db_acceso = Acceso(
        id = cadena_hasheada.decode("utf-8"),
        ultimo_login = datetime.datetime.now()
    )
    db.add(db_acceso) # Guardamos el acceso en db
    # Hasta aquí no se escriben en la base de datos, luego recién se guardan
    db.commit() # Se aceptan los cambios que se han realizado
    db.refresh(db_acceso) # Se recarga este acceso con los últimos datos
    
    # accesos[cadena_hasheada] = {
    #     "ultimo_login" : time.time_ns()
    # }
        
    # Si pones la contraseña correspondiente te mostrará el siguiente mensaje
    return {
        "msg" : "Acceso concedido",
        "token" : cadena_hasheada
    }

    
# fastapi puede crear routers para que routees las peticiones a otras entidades
# Si separas es mucho más práctico y ordenado toda la estructura
# En el proyecto hay mucho orden para que no se crucen todos en un solo archivo donde todos trabajan
# Es importante ordenarlo de esta forma

# logout
@app.get("/logout")
# Tienes que agregar la dependencia db: Session = Depends(get_db) aquí tmb para que puedas borrar usando la db
# Las dependencias se ejecutan antes de que se ejecuten el endpoint
async def logout(token : str, db: Session = Depends(get_db)):
    db_acceso = db.query(Acceso).filter(Acceso.id == token).first()
    
    if not db_acceso:
        return{
            "msg": "Token no existe"
        }
    
    # Caso de que exista lo borramos
    db.delete(db_acceso)
    db.commit() # Haz los cambios realidad
    # No se hace refresh porque ya no existe, ya no es necesario
    
    return{
        "msg" : ""
    }

app.include_router(categorias.router)
app.include_router(videojuegos.router)