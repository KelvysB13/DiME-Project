from sqlalchemy import Column, String

from models.base import Base

# Catálogo de países con código ISO y nombre

class Pais(Base):

    __tablename__ = "pais"

    codigo_pais = Column(String(2), primary_key=True)

    nombre_pais = Column(String(60), nullable=False)
