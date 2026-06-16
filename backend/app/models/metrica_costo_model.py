from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from app.models.base import Base

# Métricas de costos, comisiones y descuentos del vendedor
class Costo(Base):

    __tablename__ = "metrica_costo"

    id_metrica_costo = Column(Integer, primary_key=True, autoincrement=True)
    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)
    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")
    ventas_cobradas_total = Column(Numeric(15, 2), nullable=False, default=0.00)
    neto_recibido = Column(Numeric(15, 2), nullable=False, default=0.00)
    cargos_por_venta = Column(Numeric(15, 2), nullable=False, default=0.00)
    costos_envio = Column(Numeric(15, 2), nullable=False, default=0.00)
    inversion_ads = Column(Numeric(15, 2), nullable=False, default=0.00)
    otros_cargos = Column(Numeric(15, 2), nullable=False, default=0.00)
    cargos_envio_full = Column(Numeric(15, 2), nullable=False, default=0.00)
    descuento_reputacion = Column(Numeric(15, 2), nullable=False, default=0.00)
