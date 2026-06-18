from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.publicacion import Publicacion
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class PublicacionRepository(SQLAlchemyRepository[Publicacion]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Publicacion)
