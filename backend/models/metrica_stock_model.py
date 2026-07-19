from sqlalchemy import Column, BigInteger, DateTime, ForeignKey

from models.base import Base

# Métricas de inventario Full (espacios, calidad, productos problemáticos)

class Stock(Base):

    __tablename__ = "metrica_stock_full"

    id_metrica_stock = Column(BigInteger, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)

    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")

    espacios_p_asignados = Column(BigInteger, nullable=False, default=0)

    espacios_g_asignados = Column(BigInteger, nullable=False, default=0)

    puntaje_calidad = Column(BigInteger, nullable=False)

    productos_no_aptos_venta = Column(BigInteger, nullable=False, default=0)

    productos_sin_rotacion = Column(BigInteger, nullable=False, default=0)

    productos_antiguedad = Column(BigInteger, nullable=False, default=0)

    productos_exceso_proyeccion = Column(BigInteger, nullable=False, default=0)
