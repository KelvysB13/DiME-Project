from sqlalchemy import Column, Integer, Numeric, Date

from models.base import Base


class DiagnosticoFinanzas(Base):

    __tablename__ = "mv_diagnostico_finanzas"

    id = Column(Integer, primary_key=True)

    cvr_global = Column(Numeric(10, 2), nullable=False)

    margen_neto_real = Column(Numeric(10, 2), nullable=False)

    ticket_promedio = Column(Numeric(15, 2), nullable=False)

    carga_total_costos = Column(Numeric(10, 2), nullable=False)

    ratio_intencion_compra = Column(Numeric(10, 2), nullable=False)

    descuento_reputacion = Column(Numeric(10, 2), nullable=False)

    tasa_cobro_efectivo = Column(Numeric(10, 2), nullable=False)

    crecimiento_mom = Column(Numeric(10, 2))

    ventas_periodo_actual = Column(Integer, nullable=False)

    fecha_inicio_periodo = Column(Date, nullable=False)
    
    fecha_fin_periodo = Column(Date, nullable=False)
