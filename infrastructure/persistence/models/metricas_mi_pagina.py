from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, BigInteger
from sqlalchemy.orm import relationship, Mapped
from resources.db import Base
from infrastructure.persistence.models.soft_delete_mixin import SoftDeleteMixin


class Metricas_mi_pagina(SoftDeleteMixin, Base):
    __tablename__ = "metricas_mi_pagina"

    id_metricas_pagina: Mapped[int] = Column(BigInteger, primary_key=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor"), unique=True)
    fecha_captura = Column(String(255), default=lambda: datetime.now(timezone.utc))
    tiene_banner = Column(Boolean, default=False)
    tiene_logo = Column(Boolean, default=False)
    tiene_carruseles = Column(Boolean, default=False)
    categorias_organizadas = Column(Boolean, default=False)

    vendedor_ref: Mapped[Optional["Vendedor"]] = relationship("Vendedor", back_populates="metricas_mi_pagina", lazy="selectin", uselist=False)