from sqlalchemy.orm import Session
from infrastructure.persistence.models.metricas_stock_full import Metricas_stock_full
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_stock_fullRepository(SQLAlchemyRepository[Metricas_stock_full]):
    def __init__(self, db: Session):
        super().__init__(db, Metricas_stock_full)
