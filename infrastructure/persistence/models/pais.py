from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from typing import Optional, List
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Pais(SoftDeleteMixin, Base):
    __tablename__ = "pais"

    codigo_pais: Mapped[str] = Column(String(2), primary_key=True)
    nombre_pais = Column(String(60))

    vendedor: Mapped[List["Vendedor"]] = relationship("Vendedor", back_populates="pais_ref", lazy="selectin")