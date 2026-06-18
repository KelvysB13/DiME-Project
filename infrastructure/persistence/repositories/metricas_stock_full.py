from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.metricas_stock_full import Metricas_stock_full
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_stock_fullRepository(SQLAlchemyRepository[Metricas_stock_full]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Metricas_stock_full)
