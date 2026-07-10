from sqlalchemy import Column, BigInteger, String, Numeric

from models.base import Base


class KpiMaestro(Base):

    __tablename__ = "kpis_maestro"

    id_kpi = Column(BigInteger, primary_key=True, autoincrement=True)

    dimension = Column(String(50), nullable=False)

    nombre_kpi = Column(String(100), nullable=False, unique=True)

    operador_logico = Column(String(20), nullable=False)

    umbral_verde_inf = Column(Numeric(10, 4))

    umbral_verde_sup = Column(Numeric(10, 4))

    umbral_amarillo_inf = Column(Numeric(10, 4))

    umbral_amarillo_sup = Column(Numeric(10, 4))

    texto_ideal = Column(String(50))

    texto_alerta = Column(String(100))

    texto_peligro = Column(String(50))

    prioridad = Column(String(20), nullable=False)
