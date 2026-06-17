from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from typing import Optional, List
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Metricas_calidad_publicacion(SoftDeleteMixin, Base):
    __tablename__ = "metricas_calidad_publicacion"

    id_metricas_calidad_publi: Mapped[int] = Column(BigInteger, primary_key=True)
    id_publicacion = Column(BigInteger, ForeignKey("publicacion.id_publicacion"), unique=True)
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    cantidad_fotos = Column(Integer, default='0 CHECK')
    tiene_video = Column(Boolean, default=False)
    caracteristicas_completas = Column(Boolean, default=False)
    puntaje_calidad = Column(Integer)

    publicacion_ref: Mapped[Optional["Publicacion"]] = relationship("Publicacion", back_populates="metricas_calidad_publicacion", lazy="selectin", uselist=False)