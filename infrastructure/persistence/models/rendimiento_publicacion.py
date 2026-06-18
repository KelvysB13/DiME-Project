from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Rendimiento_publicacion(SoftDeleteMixin, Base):
    __tablename__ = "rendimiento_publicacion"

    id_rendimiento_publi: Mapped[int] = Column(BigInteger, primary_key=True)
    id_publicacion = Column(BigInteger, ForeignKey("publicacion.id_publicacion"))
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    fecha_inicio_periodo = Column(Date)
    fecha_fin_periodo = Column(Date)
    visitas = Column(Integer, default='0 CHECK')
    ventas = Column(Integer, default='0 CHECK')

    publicacion_ref: Mapped[Optional["Publicacion"]] = relationship("Publicacion", back_populates="rendimiento_publicacion", lazy="selectin", uselist=False)