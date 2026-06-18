from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.pais import Pais
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class PaisRepository(SQLAlchemyRepository[Pais]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Pais)
