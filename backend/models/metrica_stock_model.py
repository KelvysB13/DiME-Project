from sqlalchemy import Column, Integer, DateTime, ForeignKey

from models.base import Base

# Métricas de inventario Full (espacios, calidad, productos problemáticos)

class Stock(Base):

    __tablename__ = "metrica_stock_full"

    id_metrica_stock = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)

    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")

    espacios_p_asignados = Column(Integer, nullable=False, default=0)

    espacios_g_asignados = Column(Integer, nullable=False, default=0)

    puntaje_calidad = Column(Integer, nullable=False)

    productos_no_aptos_venta = Column(Integer, nullable=False, default=0)

    productos_sin_rotacion = Column(Integer, nullable=False, default=0)

    productos_antiguedad = Column(Integer, nullable=False, default=0)

    productos_exceso_proyeccion = Column(Integer, nullable=False, default=0)
