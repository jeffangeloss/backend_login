from fastapi import APIRouter, HTTPException, Header, Depends
from uuid import uuid4
from pydantic import BaseModel
from data import accesos # para dependencia circular creas data.py
# . mismo nivel
# .. nivel más arriba

class Categoria(BaseModel):
    id : str | None = None
    nombre : str

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

categorias = []

async def verify_token(x_token: str = Header(...)):
    if not x_token.encode("utf-8") in accesos:
        # Mecanismo de seguridad, token estático
        # Cuando te logeas esto te lo entregan y se guarda en el localstorage
        # Por eso, este mecanismo de seguridad es bastante básico para que sea token dinámico
        # Cada vez que te logeas se genera un único token
        # Y que cada vez que toques un endpoint estos serán capaces de poder identificar si este es un token valido

    #   investigar fecha de caducidad del token
        raise HTTPException(
            status_code=403,
            detail={
                "msg" : "Token incorreto"
            }
        )
    return x_token

@router.get("/", dependencies=[Depends(verify_token)])
async def list_categorias():
    return {
        "msg": "",
        "data": categorias
    }

@router.get("/{cat_id}", dependencies=[Depends(verify_token)])
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
@router.post("/", dependencies=[Depends(verify_token)])
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
@router.put("/", dependencies=[Depends(verify_token)])
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
@router.delete("/{categoria_id}", dependencies=[Depends(verify_token)])
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