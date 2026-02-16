from pydantic import BaseModel

class videoJuego(BaseModel):
    id : str | None = None
    nombre : str
    descripcion: str
    url_imagen: str
    categoria : "Categoria"
    class Config:
        from_attributes = True

class Categoria(BaseModel):
    id : str | None = None
    nombre : str
    videojuegos : list[videoJuego]
    class Config:
        from_attributes = True

