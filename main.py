import time
import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from routers import categorias, videojuegos
from data import accesos


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
async def login(login_request : LoginRequest):
    if login_request.username == "PROGRAWEB" and login_request.password == "123123123":
    # usaremos una librería que se encarge de encriptar
    # bcrypt    
        hora_actual = time.time_ns()
        # time_ns: nano segundos (int)
        cadena_a_encriptar = f"{login_request.username}-{str(hora_actual)}"
        cadena_hasheada = bcrypt.hashpw(
            cadena_a_encriptar.encode("utf-8"),
            bcrypt.gensalt())
        # interpolación de strings, entre llaves se incrustan
        
        accesos[cadena_hasheada] = {
            "ultimo_login" : time.time_ns()
        }
        
        # Si pones la contraseña correspondiente te mostrará el siguiente mensaje
        return {
            "msg" : "Acceso concedido",
            "token" : cadena_hasheada
        }
    else:
        raise HTTPException(
            status_code=400, 
            detail="Error en el login, credenciales incorrectas")
        # return{
        #     "msg" : "Error en login"
        # }
    
# fastapi puede crear routers para que routees las peticiones a otras entidades
# Si separas es mucho más práctico y ordenado toda la estructura
# En el proyecto hay mucho orden para que no se crucen todos en un solo archivo donde todos trabajan
# Es importante ordenarlo de esta forma

# logout
@app.get("/logout")
async def logout(token : str):
    # el token lo tenemos que enviar obligatoriamente como un query parameter
    if token.encode("utf-8") in accesos:
        # analizas si está en la lista de accesos
        # si está lo sacas, es decir le haces log out
        accesos.pop(token.encode("utf-8"))
        return{
            "msg" : ""
        }
    else:
        return{
            "msg": "Token no existe"
        }
app.include_router(categorias.router)
app.include_router(videojuegos.router)