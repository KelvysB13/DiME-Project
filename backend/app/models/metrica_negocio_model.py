from sqlalchemy import Column, Integer, Numeric, DateTime, Date, ForeignKey
from app.models.base import Base

# Métricas de negocio del vendedor (ventas, unidades, visitas)
class Negocio(Base):

    __tablename__ = "metrica_negocio"

    id_metrica_negocio = Column(Integer, primary_key=True, autoincrement=True)
    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)
    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")
    fecha_inicio_periodo = Column(Date, nullable=False)
    fecha_fin_periodo = Column(Date, nullable=False)
    ventas_brutas_moneda_local = Column(Numeric(15, 2), nullable=False, default=0.00)
    ventas_brutas_usd = Column(Numeric(15, 2), nullable=False, default=0.00)
    unidades_vendidas = Column(Integer, nullable=False, default=0)
    visitas_totales = Column(Integer, nullable=False, default=0)
    intencion_compra = Column(Integer, nullable=False, default=0)
    ventas_concretadas = Column(Integer, nullable=False, default=0)
    precio_promedio_unidad = Column(Numeric(15, 2), nullable=False, default=0.00)
    precio_promedio_venta = Column(Numeric(15, 2), nullable=False, default=0.00)
