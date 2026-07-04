from sqlalchemy import Column, Integer, Numeric, String, DateTime

from models.base import Base


class DiagnosticoReputacion(Base):

    __tablename__ = "mv_diagnostico_reputacion"

    id = Column(Integer, primary_key=True)

    tasa_reclamos = Column(Numeric(10, 2), nullable=False)

    tasa_cancelaciones = Column(Numeric(10, 2), nullable=False)

    tasa_mediaciones = Column(Numeric(10, 2), nullable=False)

    tasa_envios_incorrectos = Column(Numeric(10, 2), nullable=False)

    nivel_reputacion = Column(String(20), nullable=False)

    insignia = Column(String(20))
    
    fecha_captura = Column(DateTime(timezone=True), nullable=False)
