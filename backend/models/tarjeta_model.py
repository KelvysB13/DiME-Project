from sqlalchemy import Column, BigInteger, String, Date, ForeignKey, CheckConstraint
from models.base import Base

class Tarjeta(Base):

    __tablename__ = "tarjeta"

    id_tarjeta = Column(BigInteger, primary_key=True, autoincrement=True)
    id_vendedor = Column(BigInteger, ForeignKey("vendedor.id_vendedor", ondelete="CASCADE"), nullable=False)
    nombre_titular = Column(String(100), nullable=False)
    numero_tarjeta = Column(String(255), nullable=False)
    fecha_expiracion = Column(Date, nullable=False)
    cvv = Column(String(255), nullable=False)
    tipo_tarjeta = Column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("tipo_tarjeta IN ('Visa', 'MasterCard')", name="chk_tipo_tarjeta"),
    )
