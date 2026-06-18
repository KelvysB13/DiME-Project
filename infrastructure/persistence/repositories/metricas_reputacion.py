from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.metricas_reputacion import Metricas_reputacion
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_reputacionRepository(SQLAlchemyRepository[Metricas_reputacion]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Metricas_reputacion)
