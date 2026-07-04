from sqlalchemy import Column, Integer, String

from models.base import Base


class DiagnosticoVendedoresSemaforo(Base):

    __tablename__ = "v_diagnostico_vendedores_semaforo"

    id_vendedor = Column(Integer, primary_key=True)

    dimension = Column(String(50), nullable=False)

    nombre_kpi = Column(String(100), primary_key=True)

    prioridad = Column(String(20), nullable=False)

    valor_actual = Column(String)
    
    estado_semaforo = Column(String(10), nullable=False)
