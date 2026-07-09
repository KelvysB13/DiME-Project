from sqlalchemy import Column, Integer, BigInteger, Numeric, Text, Date, DateTime, ForeignKey

from models.base import Base


class HistDiagnosticoReputacion(Base):

    __tablename__ = "hist_diagnostico_reputacion"

    id_hist_reputacion = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False)

    tasa_reclamos = Column(Numeric)

    tasa_cancelaciones = Column(Numeric)

    tasa_mediaciones = Column(Numeric)

    tasa_envios_incorrectos = Column(Numeric)

    nivel_reputacion = Column(Text)

    insignia = Column(Text)

    fecha_captura = Column(Date)

    fecha_ingesta = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")
