from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey

from models.base import Base

# Vendedor/tienda de Mercado Libre con autenticación y plan contratado

class Vendedor(Base):

    __tablename__ = "vendedor"

    id_vendedor = Column(Integer, primary_key=True, autoincrement=True)

    user_name = Column(String(50), nullable=False, unique=True)

    nombre_tienda = Column(String(100), nullable=False)

    codigo_pais = Column(String(2), ForeignKey("pais.codigo_pais"), nullable=False)

    moneda_local = Column(String(3), ForeignKey("moneda.codigo_moneda"), nullable=False)

    tipo_plan = Column(Integer, ForeignKey("plan.id"), default=1)

    email = Column(String(255), nullable=False, unique=True)

    password_hash = Column("password_hash", String(255), nullable=False, server_default="")

    access_token = Column(Text)

    refresh_token = Column(Text)

    tiempo_token = Column(DateTime(timezone=True))

    esta_activo = Column(Boolean, nullable=False, default=True)

    fecha_creacion = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")
