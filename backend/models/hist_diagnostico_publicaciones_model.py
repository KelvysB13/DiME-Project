from sqlalchemy import Column, Integer, BigInteger, Numeric, DateTime, ForeignKey

from models.base import Base


class HistDiagnosticoPublicaciones(Base):

    __tablename__ = "hist_diagnostico_publicaciones"

    id_hist_publicaciones = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), nullable=False)

    total_publicaciones = Column(BigInteger)

    cvr_publicacion = Column(Numeric)

    pct_catalogo_completo = Column(Numeric)

    pct_publicaciones_con_video = Column(Numeric)

    fecha_ingesta = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")
