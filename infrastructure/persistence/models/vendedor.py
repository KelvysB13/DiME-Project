from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Vendedor(SoftDeleteMixin, Base):
    __tablename__ = "vendedor"

    id_vendedor: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True)
    nombre_tienda = Column(String(100))
    codigo_pais = Column(String(2), ForeignKey("pais.codigo_pais"))
    moneda_local = Column(String(3), ForeignKey("moneda.codigo_moneda"))
    tipo_plan = Column(Integer, ForeignKey("plan_saas.id_plan"), nullable=True, default=1)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255), nullable=False, default='')
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    tiempo_token = Column(String(255), nullable=True)
    esta_activo = Column(Boolean, default=True)
    fecha_creacion = Column(String(255), default=lambda: datetime.now(timezone.utc))

    @property
    def password(self) -> str:
        return self.password_hash

    @password.setter
    def password(self, value: str) -> None:
        self.password_hash = value

    pais_ref: Mapped[Optional["Pais"]] = relationship("Pais", back_populates="vendedor", lazy="selectin", uselist=False)
    moneda_ref: Mapped[Optional["Moneda"]] = relationship("Moneda", back_populates="vendedor", lazy="selectin", uselist=False)
    plan_saas_ref: Mapped[Optional["Plan_saas"]] = relationship("Plan_saas", back_populates="vendedor", lazy="selectin", uselist=False)
    publicacion: Mapped[list["Publicacion"]] = relationship("Publicacion", back_populates="vendedor_ref", lazy="selectin")
    reportes_diagnostico: Mapped[list["Reportes_diagnostico"]] = relationship("Reportes_diagnostico", back_populates="vendedor_ref", lazy="selectin")
    metricas_reputacion: Mapped[Optional["Metricas_reputacion"]] = relationship("Metricas_reputacion", back_populates="vendedor_ref", uselist=False, lazy="selectin")
    metricas_negocio: Mapped[Optional["Metricas_negocio"]] = relationship("Metricas_negocio", back_populates="vendedor_ref", uselist=False, lazy="selectin")
    metricas_costo: Mapped[Optional["Metricas_costo"]] = relationship("Metricas_costo", back_populates="vendedor_ref", uselist=False, lazy="selectin")
    metricas_stock_full: Mapped[Optional["Metricas_stock_full"]] = relationship("Metricas_stock_full", back_populates="vendedor_ref", uselist=False, lazy="selectin")
    metricas_mi_pagina: Mapped[Optional["Metricas_mi_pagina"]] = relationship("Metricas_mi_pagina", back_populates="vendedor_ref", uselist=False, lazy="selectin")