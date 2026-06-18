from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.moneda import Moneda
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class MonedaRepository(SQLAlchemyRepository[Moneda]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Moneda)
