from sqlalchemy import Column, Integer, Text, Date, ForeignKey

from sqlalchemy.dialects.postgresql import JSONB

from models.base import Base

# Reporte de diagnóstico generado para un vendedor

class Reporte(Base):

    __tablename__ = "reporte_diagnostico"

    id_reporte = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor"), nullable=False)

    fecha_generacion = Column(Date, nullable=False, server_default="CURRENT_DATE")

    fecha_inicio_periodo = Column(Date, nullable=False)

    fecha_fin_periodo = Column(Date, nullable=False)

    resumen_ejecutivo = Column(Text)

    plan_accion = Column(JSONB, nullable=False, default="{}")
