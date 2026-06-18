from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.metricas_costo import Metricas_costo
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_costoRepository(SQLAlchemyRepository[Metricas_costo]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Metricas_costo)
