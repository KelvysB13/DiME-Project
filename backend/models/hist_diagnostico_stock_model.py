from sqlalchemy import Column, Integer, BigInteger, Numeric, DateTime, ForeignKey

from models.base import Base


class HistDiagnosticoStock(Base):

    __tablename__ = "hist_diagnostico_stock"

    id_hist_stock = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False)

    dead_stock_rate = Column(Numeric)

    antiguedad_riesgo = Column(Numeric)

    productos_no_aptos = Column(Numeric)

    overstock_rate = Column(Numeric)

    utilizacion_espacios = Column(Numeric)

    puntaje_calidad = Column(Numeric)

    fecha_ingesta = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")
