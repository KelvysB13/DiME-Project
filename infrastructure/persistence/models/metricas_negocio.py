from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Numeric, Date, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from typing import Optional, List
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Metricas_negocio(SoftDeleteMixin, Base):
    __tablename__ = "metricas_negocio"

    id_metricas_negocio: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), unique=True)
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    fecha_inicio_periodo = Column(Date)
    fecha_fin_periodo = Column(Date)
    ventas_brutas_moneda_local = Column(Numeric(15,2), default='0.00 CHECK')
    ventas_brutas_usd = Column(Numeric(15,2), default='0.00 CHECK')
    unidades_vendidas = Column(Integer, default='0 CHECK')
    visitas_totales = Column(Integer, default='0 CHECK')
    intencion_compra = Column(Integer, default='0 CHECK')
    ventas_concretadas = Column(Integer, default='0 CHECK')
    precio_promedio_unidad = Column(Numeric(15,2), default='0.00 CHECK')
    precio_promedio_venta = Column(Numeric(15,2), default='0.00 CHECK')

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="metricas_negocio", lazy="selectin", uselist=False)