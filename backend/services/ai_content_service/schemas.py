from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ObjetivoCampanaInput(BaseModel):
    nombreProducto: str
    descripcionProducto: str

class PresupuestoDuracionInput(BaseModel):
    nombreProducto: str
    tipoCampana: str  # Pequeña, Mediana, Grande
    duracion: str  # Corta, Mediana, Larga

class PublicoObjetivoUbicacionesInput(BaseModel):
    nombreProducto: str
    descripcionProducto: str
    distrito: str
    provincia: str
    departamento: str

class FormatoCTAInput(BaseModel):
    nombreProducto: str
    descripcionProducto: str

class ContenidoCreativoInput(BaseModel):
    nombreProducto: str
    descripcionProducto: str
    publicoObjetivo: str
    tonoEstilo: str  # Por ejemplo, 'casual y juvenil', 'profesional y serio'

class EncabezadoAnuncio(BaseModel):
    nombreProducto: str
    descripcionProducto: str
    palabrasClave: List[str]  # Cambiado a List[str]
    estiloEscritura: str
    longitudMaxima: int
    variantes: int  # Número de variantes a generar

class CampanaDetallesInput(BaseModel):
    nombreProducto: str
    descripcionProducto: str
    tipoCampana: str  # Por ejemplo: Pequeña, Mediana, Grande
    duracionPreferida: str  # Por ejemplo: Corta, Mediana, Larga

class DocumentoCreate(BaseModel):
    tipo_documento: str = Field(..., example="Artículo")
    contenido: str = Field(..., example="Contenido del documento...")

class DocumentoResponse(BaseModel):
    id_documento: int
    tipo_documento: str
    contenido: str
    fecha_creacion: datetime
    id_usuario: int

    class Config:
        from_attributes = True