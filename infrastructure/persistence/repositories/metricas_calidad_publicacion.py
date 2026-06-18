from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.metricas_calidad_publicacion import Metricas_calidad_publicacion
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_calidad_publicacionRepository(SQLAlchemyRepository[Metricas_calidad_publicacion]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Metricas_calidad_publicacion)
