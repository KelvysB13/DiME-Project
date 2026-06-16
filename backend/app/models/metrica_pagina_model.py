from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from app.models.base import Base

# Métricas de la página del vendedor (banner, logo, carruseles)
class Pagina(Base):

    __tablename__ = "metrica_mi_pagina"

    id_metrica_pagina = Column(Integer, primary_key=True, autoincrement=True)
    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor"), nullable=False, unique=True)
    fecha_captura = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")
    tiene_banner = Column(Boolean, nullable=False, default=False)
    tiene_logo = Column(Boolean, nullable=False, default=False)
    tiene_carruseles = Column(Boolean, nullable=False, default=False)
    categorias_organizadas = Column(Boolean, nullable=False, default=False)
