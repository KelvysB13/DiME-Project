from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from models.base import Base

class Admin(Base):
    
    __tablename__ = "admin"

    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    access_token = Column(Text)
    tiempo_token = Column(DateTime(timezone=True), nullable=True)
    refresh_token = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), nullable=False, server_default="CURRENT_TIMESTAMP")
    esta_activo = Column(Boolean, nullable=False, default=True)