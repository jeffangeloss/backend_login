from fastapi import APIRouter
from pydantic import BaseModel

from ..routers.categorias import Categoria


router = APIRouter(
    prefix="/videojuegos",
    tags=["Videojuegos"]
)

videojuegos = []

# Un videojuego a una categoría, pero también una categoría puede estar en varios videojuegos, entonces es una relación de muchos a muchos, 
# pero para simplificarlo, vamos a hacer que un videojuego solo tenga una categoría, pero una categoría puede estar en varios videojuegos

@router.get("/")
async def list_videojuegos():
    return {
        "msg" : "",
        "data" : videojuegos
    }