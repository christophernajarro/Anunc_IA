from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .handlers import (
    manejar_definir_campana,
    manejar_definir_publico_ubicaciones,
    manejar_elegir_formato_cta,
    manejar_crear_contenido_creativo,
    manejar_create_heading
)
from .schemas import (
    CampanaDetallesInput,
    PublicoObjetivoUbicacionesInput,
    FormatoCTAInput,
    ContenidoCreativoInput,
    EncabezadoAnuncio
)
from ..auth_service.security import get_current_user
from common.models.usuario import Usuario
from common.database.database import get_db

router = APIRouter()

@router.post("/definir_campana", summary="Definir objetivo de campaña y detalles")
async def definir_campana_endpoint(
    data: CampanaDetallesInput,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Usuario ID: {current_user.id_usuario} | Datos recibidos en /definir_campana: {data.dict()}")
    return await manejar_definir_campana(data, current_user, db)

@router.post("/definir_publico_ubicaciones", summary="Definir público objetivo y ubicaciones")
async def definir_publico_ubicaciones_endpoint(
    data: PublicoObjetivoUbicacionesInput,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Usuario ID: {current_user.id_usuario} | Datos recibidos en /definir_publico_ubicaciones: {data.dict()}")
    return await manejar_definir_publico_ubicaciones(data, current_user, db)

@router.post("/elegir_formato_cta", summary="Elegir formato y CTA")
async def elegir_formato_cta_endpoint(
    data: FormatoCTAInput,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Usuario ID: {current_user.id_usuario} | Datos recibidos en /elegir_formato_cta: {data.dict()}")
    return await manejar_elegir_formato_cta(data, current_user, db)

@router.post("/crear_contenido_creativo", summary="Crear contenido creativo")
async def crear_contenido_creativo_endpoint(
    data: ContenidoCreativoInput,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Usuario ID: {current_user.id_usuario} | Datos recibidos en /crear_contenido_creativo: {data.dict()}")
    return await manejar_crear_contenido_creativo(data, current_user, db)

@router.post("/create_heading", summary="Generar encabezados de anuncio")
async def create_heading_endpoint(
    encabezado: EncabezadoAnuncio,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Usuario ID: {current_user.id_usuario} | Datos recibidos en /create_heading: {encabezado.dict()}")
    return await manejar_create_heading(encabezado, current_user, db)
