from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text, BigInteger, JSON
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Reportes_diagnostico(SoftDeleteMixin, Base):
    __tablename__ = "reportes_diagnostico"

    id_reporte: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"))
    fecha_generacion = Column(Date, default=lambda: datetime.now(timezone.utc))
    fecha_inicio_periodo = Column(Date)
    fecha_fin_periodo = Column(Date)
    resumen_ejecutivo = Column(Text, nullable=True)
    plan_accion = Column(JSON, default='{}')

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="reportes_diagnostico", lazy="selectin", uselist=False)