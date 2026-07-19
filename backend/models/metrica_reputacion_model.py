from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey

from models.base import Base

# Métricas de reputación del vendedor (reclamos, cancelaciones, nivel)

class Reputacion(Base):

    __tablename__ = "metrica_reputacion"

    id_metrica_reputacion = Column(BigInteger, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)

    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")

    ventas_totales_periodo = Column(BigInteger, nullable=False, default=0)

    total_reclamos = Column(BigInteger, nullable=False, default=0)

    total_mediaciones = Column(BigInteger, nullable=False, default=0)

    total_canceladas = Column(BigInteger, nullable=False, default=0)

    total_envios_incorrectos = Column(BigInteger, nullable=False, default=0)

    nivel_reputacion = Column(String(20), nullable=False)

    insignia = Column(String(20))
