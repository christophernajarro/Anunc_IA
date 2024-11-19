from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from common.database.database import get_db
from common.models.usuario import Usuario
from common.schemas.usuario import UsuarioResponse, UsuarioUpdate
from datetime import datetime, timezone
from services.auth_service.security import get_password_hash, get_current_user

router = APIRouter()

@router.get("/{id_usuario}", response_model=UsuarioResponse, summary="Obtener información de un usuario")
def obtener_usuario(id_usuario: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este recurso.")
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return db_usuario

@router.put("/{id_usuario}", response_model=UsuarioResponse, summary="Actualizar información del usuario")
def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permisos para modificar este usuario.")
    
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    if usuario.email:
        # Verificar si el nuevo email ya está en uso
        email_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
        if email_existente and email_existente.id_usuario != id_usuario:
            raise HTTPException(status_code=400, detail="El email ya está registrado por otro usuario.")
        db_usuario.email = usuario.email
    
    if usuario.password:
        hashed_password = get_password_hash(usuario.password)
        db_usuario.contraseña = hashed_password
    
    if usuario.nombre is not None:
        db_usuario.nombre = usuario.nombre
    if usuario.bio is not None:
        db_usuario.bio = usuario.bio
    if usuario.avatar_url is not None:
        db_usuario.avatar_url = usuario.avatar_url
    
    db_usuario.fecha_actualizacion_perfil = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario

@router.delete("/{id_usuario}", status_code=status.HTTP_200_OK, summary="Eliminar un usuario")
def eliminar_usuario(id_usuario: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id_usuario != id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar este usuario.")
    
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    db.delete(db_usuario)
    db.commit()
    
    return {"msg": "Usuario eliminado exitosamente."}
