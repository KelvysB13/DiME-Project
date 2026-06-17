from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from typing import Optional, List
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Moneda(SoftDeleteMixin, Base):
    __tablename__ = "moneda"

    codigo_moneda: Mapped[str] = Column(String(3), primary_key=True)
    nombre_moneda = Column(String(50))
    simbolo = Column(String(5))

    vendedor: Mapped[List["Vendedor"]] = relationship("Vendedor", back_populates="moneda_ref", lazy="selectin")