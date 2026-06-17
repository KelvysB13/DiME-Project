from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Numeric, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from typing import Optional, List
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Metricas_costo(SoftDeleteMixin, Base):
    __tablename__ = "metricas_costo"

    id_metricas_costo: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), unique=True)
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    ventas_cobradas_total = Column(Numeric(15,2), default=0.0)
    neto_recibido = Column(Numeric(15,2), default=0.0)
    cargos_por_venta = Column(Numeric(15,2), default='0.00 CHECK')
    costos_envio = Column(Numeric(15,2), default='0.00 CHECK')
    inversion_ads = Column(Numeric(15,2), default='0.00 CHECK')
    otros_cargos = Column(Numeric(15,2), default='0.00 CHECK')
    cargos_envio_full = Column(Numeric(15,2), default='0.00 CHECK')
    descuento_reputacion = Column(Numeric(15,2), default=0.0)

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="metricas_costo", lazy="selectin", uselist=False)