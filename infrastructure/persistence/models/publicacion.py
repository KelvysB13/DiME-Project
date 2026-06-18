from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Publicacion(SoftDeleteMixin, Base):
    __tablename__ = "publicacion"

    id_publicacion: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"))
    ml_item_id = Column(String(20), unique=True)
    titulo = Column(String(100))
    tipo_publicacion = Column(String(20))
    estado_publicacion = Column(String(20))

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="publicacion", lazy="selectin", uselist=False)
    rendimiento_publicacion: Mapped[list["Rendimiento_publicacion"]] = relationship("Rendimiento_publicacion", back_populates="publicacion_ref", lazy="selectin")
    metricas_calidad_publicacion: Mapped[Optional["Metricas_calidad_publicacion"]] = relationship("Metricas_calidad_publicacion", back_populates="publicacion_ref", uselist=False, lazy="selectin")