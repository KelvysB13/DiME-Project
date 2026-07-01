from sqlalchemy import Column, Integer, Numeric

from models.base import Base


class DiagnosticoAds(Base):

    __tablename__ = "mv_diagnostico_ads"

    id = Column(Integer, primary_key=True)

    roas = Column(Numeric(10, 2), nullable=False)

    acos = Column(Numeric(10, 2), nullable=False)

    inversion_ads_sobre_ventas = Column(Numeric(10, 2), nullable=False)
    
    inversion_ads = Column(Numeric(15, 2), nullable=False)
