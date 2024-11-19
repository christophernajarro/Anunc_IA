from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from common.database.database import get_db
from common.models.usuario import Usuario
from ..ai_content_service.models import Documento
from services.document_service.schemas import DocumentoCreate, DocumentoUpdate, DocumentoResponse
from services.auth_service.security import get_current_user
from datetime import datetime, timezone

router = APIRouter()

@router.post("/", response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo documento")
def crear_documento(documento: DocumentoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    nuevo_documento = Documento(
        tipo_documento=documento.tipo_documento,
        contenido=documento.contenido,
        id_usuario=current_user.id_usuario,
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_documento)
    return nuevo_documento

@router.get("/{id_documento}", response_model=DocumentoResponse, summary="Obtener información de un documento")
def obtener_documento(id_documento: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    documento = db.query(Documento).filter(Documento.id_documento == id_documento, Documento.id_usuario == current_user.id_usuario).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    return documento

@router.get("/", response_model=list[DocumentoResponse], summary="Obtener todos los documentos del usuario")
def listar_documentos(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    documentos = db.query(Documento).filter(Documento.id_usuario == current_user.id_usuario).all()
    return documentos

@router.put("/{id_documento}", response_model=DocumentoResponse, summary="Actualizar un documento existente")
def actualizar_documento(id_documento: int, documento_update: DocumentoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    documento = db.query(Documento).filter(Documento.id_documento == id_documento, Documento.id_usuario == current_user.id_usuario).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    
    if documento_update.tipo_documento is not None:
        documento.tipo_documento = documento_update.tipo_documento
    if documento_update.contenido is not None:
        documento.contenido = documento_update.contenido
    
    db.commit()
    db.refresh(documento)
    return documento

@router.delete("/{id_documento}", status_code=status.HTTP_200_OK, summary="Eliminar un documento")
def eliminar_documento(id_documento: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    documento = db.query(Documento).filter(Documento.id_documento == id_documento, Documento.id_usuario == current_user.id_usuario).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    
    db.delete(documento)
    db.commit()
    return {"msg": "Documento eliminado exitosamente."}