from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

def obtener_productos_por_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Producto).filter(models.Producto.id_usuario == usuario_id).offset(skip).limit(limit).all()

def crear_producto(db: Session, producto: schemas.ProductoCreate, usuario_id: int):
    nuevo_producto = models.Producto(**producto.dict(), id_usuario=usuario_id)
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

def obtener_producto(db: Session, producto_id: int, usuario_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id, models.Producto.id_usuario == usuario_id).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto

def actualizar_producto(db: Session, producto_id: int, producto_update: schemas.ProductoUpdate, usuario_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id, models.Producto.id_usuario == usuario_id).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    for var, value in vars(producto_update).items():
        if value is not None:
            setattr(producto, var, value)
    
    db.commit()
    db.refresh(producto)
    return producto

def eliminar_producto(db: Session, producto_id: int, usuario_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id_producto == producto_id, models.Producto.id_usuario == usuario_id).first()
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    db.delete(producto)
    db.commit()
    return {"detail": "Producto eliminado exitosamente"}