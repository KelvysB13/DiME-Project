from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.vendedor import Vendedor
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class VendedorRepository(SQLAlchemyRepository[Vendedor]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Vendedor)
