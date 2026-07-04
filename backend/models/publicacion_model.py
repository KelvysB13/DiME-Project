from sqlalchemy import Column, String, Integer, ForeignKey

from models.base import Base

# Publicación/item de Mercado Libre perteneciente a un vendedor

class Publicacion(Base):

    __tablename__ = "publicacion"

    id_publicacion = Column(Integer, primary_key=True, autoincrement=True)

    id_vendedor = Column(Integer, ForeignKey("vendedor.id_vendedor", ondelete="CASCADE"), nullable=False)

    ml_item_id = Column(String(20), nullable=False, unique=True)

    titulo = Column(String(100), nullable=False)

    tipo_publicacion = Column(String(20), nullable=False)

    estado_publicacion = Column(String(20), nullable=False)
