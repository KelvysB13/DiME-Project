from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from models.base import Base

# Métricas de reputación del vendedor (reclamos, cancelaciones, nivel)

class Reputacion(Base):

    __tablename__ = "metrica_reputacion"

    id_metrica_reputacion = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)

    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")

    ventas_totales_periodo = Column(Integer, nullable=False, default=0)

    total_reclamos = Column(Integer, nullable=False, default=0)

    total_mediaciones = Column(Integer, nullable=False, default=0)

    total_canceladas = Column(Integer, nullable=False, default=0)

    total_envios_incorrectos = Column(Integer, nullable=False, default=0)

    nivel_reputacion = Column(String(20), nullable=False)

    insignia = Column(String(20))
