from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from common.database.database import Base
from datetime import datetime, timezone

class Documento(Base):
    __tablename__ = "documentos"

    id_documento = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    tipo_documento = Column(String, nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # Relación de vuelta con Usuario
    usuario = relationship("Usuario", back_populates="documentos")