from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from routers import categorias
from routers import videojuegos

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
        # Si pones la contraseña correspondiente te mostrará el siguiente mensaje
        return {
            "msg" : "Acceso concedido"
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
app.include_router(categorias.router)
app.include_router(videojuegos.router)