from sqlalchemy import Column, Integer, String, Text, Numeric

from sqlalchemy.dialects.postgresql import JSONB

from models.base import Base

# Planes SaaS (Free, Básico, Premium) con precio, límites y features

class Plan(Base):

    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)

    nombre_plan = Column(String(50), nullable=False)

    precio_mensual = Column(Numeric(10, 2), nullable=False, default=0.00)

    limite_publicaciones = Column(Integer)

    limite_metricas_dias = Column(Integer, nullable=False, default=30)

    features = Column(JSONB, nullable=False, default="[]")

    descripcion = Column(Text)
