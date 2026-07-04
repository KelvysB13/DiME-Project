from sqlalchemy import Column, Integer, DateTime, Date, ForeignKey

from models.base import Base

# Rendimiento individual de una publicación (visitas, ventas por período)

class Rendimiento(Base):

    __tablename__ = "rendimiento_publicacion"

    id_rendimiento_publi = Column(Integer, primary_key=True, autoincrement=True)

    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion", ondelete="CASCADE"), nullable=False)

    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")

    fecha_inicio_periodo = Column(Date, nullable=False)

    fecha_fin_periodo = Column(Date, nullable=False)

    visitas = Column(Integer, nullable=False, default=0)

    ventas = Column(Integer, nullable=False, default=0)
