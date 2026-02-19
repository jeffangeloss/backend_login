from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..models import Videojuego
from app.database import get_db
from .security import verify_token


router = APIRouter(
    prefix="/videojuegos",
    tags=["Videojuegos"]
)

# Un videojuego a una categoría, pero también una categoría puede estar en varios videojuegos, entonces es una relación de muchos a muchos, 
# pero para simplificarlo, vamos a hacer que un videojuego solo tenga una categoría, pero una categoría puede estar en varios videojuegos

@router.get("/", dependencies= [Depends(verify_token)])
async def list_videojuegos(db: Session = Depends(get_db)):
    db_videojuegos = db.query(Videojuego).all()
    
    return {
        "msg" : "",
        "data" : db_videojuegos
    }