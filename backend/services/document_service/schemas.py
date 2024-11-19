from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class DocumentoCreate(BaseModel):
    tipo_documento: str = Field(..., example="Informe")
    contenido: str = Field(..., example="Contenido del documento...")

    @validator('tipo_documento')
    def tipo_valido(cls, v):
        tipos_permitidos = ["Informe", "Reporte", "Resumen"]
        if v not in tipos_permitidos:
            raise ValueError(f"tipo_documento debe ser uno de {tipos_permitidos}")
        return v

class DocumentoUpdate(BaseModel):
    tipo_documento: Optional[str] = Field(None, example="Reporte")
    contenido: Optional[str] = Field(None, example="Contenido actualizado del documento...")

    @validator('tipo_documento')
    def tipo_valido(cls, v):
        if v is not None:
            tipos_permitidos = ["Informe", "Reporte", "Resumen"]
            if v not in tipos_permitidos:
                raise ValueError(f"tipo_documento debe ser uno de {tipos_permitidos}")
        return v

class DocumentoResponse(BaseModel):
    id_documento: int
    tipo_documento: str
    contenido: str
    fecha_creacion: datetime
    id_usuario: int

    class Config:
        from_attributes = True