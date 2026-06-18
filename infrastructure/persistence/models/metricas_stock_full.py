from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Metricas_stock_full(SoftDeleteMixin, Base):
    __tablename__ = "metricas_stock_full"

    id_metricas_stock: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), unique=True)
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    espacios_p_asignados = Column(Integer, default='0 CHECK')
    espacios_g_asignados = Column(Integer, default='0 CHECK')
    puntaje_calidad = Column(Integer)
    productos_no_aptos_venta = Column(Integer, default='0 CHECK')
    productos_sin_rotacion = Column(Integer, default='0 CHECK')
    productos_antiguedad = Column(Integer, default='0 CHECK')
    productos_exceso_proyeccion = Column(Integer, default='0 CHECK')

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="metricas_stock_full", lazy="selectin", uselist=False)