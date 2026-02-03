from fastapi import APIRouter
from pydantic import BaseModel

class videoJuego(BaseModel):
    id : str | None = None
    nombre : str
    descripcion: str
    url_imagen: str
    categoria : str

router = APIRouter(
    prefix="/videojuegos",
    tags=["Videojuegos"]
)

videojuegos = []

@router.get("/")
async def list_videojuegos():
    return {
        "msg" : "",
        "data" : videojuegos
    }