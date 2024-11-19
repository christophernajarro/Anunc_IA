from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from common.database.database import Base
from datetime import datetime, timezone


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    caracteristicas = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, onupdate=datetime.now(timezone.utc))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="productos")