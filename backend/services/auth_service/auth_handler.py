from sqlalchemy.orm import Session
from .models import Usuario
from .schemas import RegisterRequest
from .security import get_password_hash
from fastapi import HTTPException

def register_user(db: Session, user: RegisterRequest) -> Usuario:
    # Verificar si el email ya está registrado
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Crear un nuevo usuario
    hashed_password = get_password_hash(user.password)
    nuevo_usuario = Usuario(
        nombre=user.nombre,
        email=user.email,
        contraseña=hashed_password
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario