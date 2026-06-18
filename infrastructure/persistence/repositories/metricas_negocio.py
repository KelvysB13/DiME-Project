from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.metricas_negocio import Metricas_negocio
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_negocioRepository(SQLAlchemyRepository[Metricas_negocio]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Metricas_negocio)
