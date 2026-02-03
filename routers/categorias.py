from fastapi import APIRouter, HTTPException
from uuid import uuid4
from pydantic import BaseModel

class Categoria(BaseModel):
    id : str | None = None
    nombre : str

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

categorias = []

@router.get("/")
async def list_categorias():
    return {
        "msg": "",
        "data": categorias
    }

@router.get("/{cat_id}")
async def get_categoria(cat_id: str):
    for cat in categorias:
        if cat.id == cat_id:
            return {
                "msg" : "",
                "data" : cat
            }
    raise HTTPException(
        status_code=404,
        detail="categoria id not found"
    )

# Objeto json que se enviará por el cuerpo de la petición
@router.post("/")
async def create_categoria(categoria: Categoria):
    categoria.id = str(uuid4())
    # TO.DO: Trabajar con una base de datos
    categorias.append(categoria)
    return {
        "msg" : "",
        "data" : categoria
    }
    
# Muchas personas se conectan a la vez, en el mismo momento
# Tú mismo quieres que el backend genere el uuid → es por eso es que tú desde el cliente NO tienes
# que enviarle el uuid
# pero si quieres modificar o eliminar... aquí si tienes que pasarle
# Creación es None → si lo vas a editar será str

# Enpoint que reciba peticiones del tipo put
# Para fines técnicos son iguales que las peticiones post
# Técnicamente son exactamente igual, solo cambia de nombre
# Es decir que al igual, se envía en el cuerpo de la petición
@router.put("/")
async def update_categoria(categoria: Categoria): # Actualizas una categoría que ya existe
    # Buscar en la lista de categorias y encontrar esa categoria
    for cat in categorias:
        if cat.id == categoria.id:
            # Se encontró categoria
            cat.nombre = categoria.nombre
            return {
                "msg" : "",
                "data" : cat
            }
    raise HTTPException(
        status_code=404, # 404 si no te acuerdas, código genérico del cliente, hay más específicos
        detail="Category id doesn't exist"
    )

# Ahora vamos a eliminar
# Pasar como path parameter
@router.delete("/{categoria_id}")
async def delete_categoria(categoria_id: str):
    for i, cat in enumerate(categorias):
        if cat.id == categoria_id:
            categorias.pop(i)
            return {
                "msg" : "",
            }
    raise HTTPException(
        status_code=404,
        detail="Cannot delete the category: Not Found"
    )