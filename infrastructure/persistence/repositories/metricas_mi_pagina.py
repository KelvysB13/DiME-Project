from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.metricas_mi_pagina import Metricas_mi_pagina
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_mi_paginaRepository(SQLAlchemyRepository[Metricas_mi_pagina]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Metricas_mi_pagina)
