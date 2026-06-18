from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Metricas_reputacion(SoftDeleteMixin, Base):
    __tablename__ = "metricas_reputacion"

    id_metricas_reputacion: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), unique=True)
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    ventas_totales_periodo = Column(Integer, default='0 CHECK')
    total_reclamos = Column(Integer, default='0 CHECK')
    total_mediaciones = Column(Integer, default='0 CHECK')
    total_canceladas = Column(Integer, default='0 CHECK')
    total_envios_incorrectos = Column(Integer, default='0 CHECK')
    nivel_reputacion = Column(String(20))
    insignia = Column(String(20), nullable=True)

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="metricas_reputacion", lazy="selectin", uselist=False)