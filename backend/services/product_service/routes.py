from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from common.database.database import get_db
from services.product_service import schemas, handlers
from common.models.usuario import Usuario
from services.auth_service.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductoOut], summary="Listar productos del usuario")
def listar_productos(skip: int = 0, limit: int = 10, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    productos = handlers.obtener_productos_por_usuario(db, current_user.id_usuario, skip, limit)
    return productos

@router.post("/", response_model=schemas.ProductoOut, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo producto")
def crear_nuevo_producto(producto: schemas.ProductoCreate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    nuevo_producto = handlers.crear_producto(db, producto, current_user.id_usuario)
    return nuevo_producto

@router.get("/{producto_id}", response_model=schemas.ProductoOut, summary="Obtener un producto específico")
def obtener_un_producto(producto_id: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    producto = handlers.obtener_producto(db, producto_id, current_user.id_usuario)
    return producto

@router.put("/{producto_id}", response_model=schemas.ProductoOut, summary="Actualizar un producto")
def actualizar_un_producto(producto_id: int, producto_update: schemas.ProductoUpdate, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    producto = handlers.actualizar_producto(db, producto_id, producto_update, current_user.id_usuario)
    return producto

@router.delete("/{producto_id}", status_code=status.HTTP_200_OK, summary="Eliminar un producto")
def eliminar_un_producto(producto_id: int, current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    resultado = handlers.eliminar_producto(db, producto_id, current_user.id_usuario)
    return resultado