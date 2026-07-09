from sqlalchemy import Column, Integer, BigInteger, Numeric, Date, DateTime, ForeignKey

from models.base import Base


class HistDiagnosticoFinanzas(Base):

    __tablename__ = "hist_diagnostico_finanzas"

    id_hist_finanzas = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False)

    cvr_global = Column(Numeric)

    margen_neto_real = Column(Numeric)

    ticket_promedio = Column(Numeric)

    carga_total_costos = Column(Numeric)

    ratio_intencion_compra = Column(Numeric)

    descuento_reputacion = Column(Numeric)

    tasa_cobro_efectivo = Column(Numeric)

    crecimiento_mom = Column(Numeric)

    ventas_periodo_actual = Column(Numeric)

    fecha_inicio_periodo = Column(Date)

    fecha_fin_periodo = Column(Date)

    fecha_ingesta = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")
