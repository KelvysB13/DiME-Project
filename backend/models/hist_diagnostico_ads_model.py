from sqlalchemy import Column, Integer, BigInteger, Numeric, DateTime, ForeignKey

from models.base import Base


class HistDiagnosticoAds(Base):

    __tablename__ = "hist_diagnostico_ads"

    id_hist_ads = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False)

    roas = Column(Numeric)

    acos = Column(Numeric)

    inversion_ads_sobre_ventas = Column(Numeric)

    inversion_ads = Column(Numeric)

    fecha_ingesta = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")
