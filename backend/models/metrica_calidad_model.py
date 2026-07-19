from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey

from models.base import Base

# Métricas de calidad de una publicación (fotos, video, puntuación)

class Calidad(Base):

    __tablename__ = "metrica_calidad_publicacion"

    id_metrica_calidad_publi = Column(BigInteger, primary_key=True, autoincrement=True)

    id_publicacion = Column(BigInteger, ForeignKey("publicacion.id_publicacion"), nullable=False, unique=True)

    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")

    cantidad_fotos = Column(BigInteger, nullable=False, default=0)

    tiene_video = Column(Boolean, nullable=False, default=False)

    caracteristicas_completas = Column(Boolean, nullable=False, default=False)

    puntaje_calidad = Column(BigInteger, nullable=False)
