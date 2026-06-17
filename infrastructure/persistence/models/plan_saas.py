from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from typing import Optional, List
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Plan_saas(SoftDeleteMixin, Base):
    __tablename__ = "plan_saas"

    id_plan: Mapped[int] = Column(Integer, primary_key=True)
    nombre_plan = Column(String(50))
    descripcion = Column(Text, nullable=True)

    vendedor: Mapped[List["Vendedor"]] = relationship("Vendedor", back_populates="plan_saas_ref", lazy="selectin")