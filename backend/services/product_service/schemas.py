from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str = Field(..., example="Laptop")
    descripcion: Optional[str] = Field(None, example="Laptop de 15 pulgadas")
    caracteristicas: Optional[str] = Field(None, example="Procesador Intel i7, 16GB RAM, 1TB SSD")
    precio: float = Field(..., gt=0, example=999.99)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, example="Laptop Pro")
    descripcion: Optional[str] = Field(None, example="Laptop de 17 pulgadas")
    caracteristicas: Optional[str] = Field(None, example="Procesador Intel i9, 32GB RAM, 2TB SSD")
    precio: Optional[float] = Field(None, gt=0, example=1299.99)

class ProductoOut(ProductoBase):
    id_producto: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    id_usuario: int

    class Config:
        from_attributes = True