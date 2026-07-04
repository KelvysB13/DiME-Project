from sqlalchemy import Column, Integer, Numeric

from models.base import Base


class DiagnosticoPublicaciones(Base):

    __tablename__ = "mv_diagnostico_publicaciones"

    id = Column(Integer, primary_key=True)

    total_publicaciones = Column(Integer, nullable=False)

    cvr_publicacion = Column(Numeric(10, 2), nullable=False)

    pct_catalogo_completo = Column(Numeric(10, 2), nullable=False)
    
    pct_publicaciones_con_video = Column(Numeric(10, 2), nullable=False)
