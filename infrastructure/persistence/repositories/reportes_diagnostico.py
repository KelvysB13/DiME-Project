from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.reportes_diagnostico import Reportes_diagnostico
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Reportes_diagnosticoRepository(SQLAlchemyRepository[Reportes_diagnostico]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Reportes_diagnostico)
