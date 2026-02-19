import datetime
from fastapi import Depends, HTTPException, Header
from ..models import Acceso
from sqlalchemy.orm import Session
from ..database import get_db


async def verify_token(x_token : str = Header(...), db: Session = Depends(get_db)):
    db_query = db.query(Acceso).filter(Acceso.id == x_token)
    db_acceso = db_query.first()
    if not db_acceso:
        raise HTTPException(
            status_code=403,
            detail={
                "msg" : "Token incorrecto"
            }
        )
    
    db_query.update({
        "ultimo_login" : datetime.datetime.now()
    })
    db.commit()
    db.refresh(db_acceso)

    return x_token
