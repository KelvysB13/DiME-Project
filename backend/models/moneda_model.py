from sqlalchemy import Column, String

from models.base import Base

# Catálogo de monedas con código, nombre y símbolo

class Moneda(Base):

    __tablename__ = "moneda"

    codigo_moneda = Column(String(3), primary_key=True)

    nombre_moneda = Column(String(50), nullable=False)

    simbolo = Column(String(5), nullable=False)
