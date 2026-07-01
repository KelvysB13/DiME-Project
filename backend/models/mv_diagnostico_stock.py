from sqlalchemy import Column, Integer, Numeric

from models.base import Base


class DiagnosticoStock(Base):

    __tablename__ = "mv_diagnostico_stock"

    id = Column(Integer, primary_key=True)

    dead_stock_rate = Column(Numeric(10, 2), nullable=False)

    antiguedad_riesgo = Column(Numeric(10, 2), nullable=False)

    productos_no_aptos = Column(Numeric(10, 2), nullable=False)

    overstock_rate = Column(Numeric(10, 2), nullable=False)

    utilizacion_espacios = Column(Numeric(10, 2), nullable=False)
    
    puntaje_calidad = Column(Integer, nullable=False)
