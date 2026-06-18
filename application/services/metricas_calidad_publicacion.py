from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.metricas_calidad_publicacion import Metricas_calidad_publicacion
from infrastructure.persistence.repositories.metricas_calidad_publicacion import Metricas_calidad_publicacionRepository
from application.services.base import BaseService
from application.dto.metricas_calidad_publicacion import Metricas_calidad_publicacionCreate, Metricas_calidad_publicacionUpdate


class Metricas_calidad_publicacionService(BaseService[Metricas_calidad_publicacionRepository, Metricas_calidad_publicacionCreate, Metricas_calidad_publicacionUpdate]):

    def __init__(self, repository: Metricas_calidad_publicacionRepository):
        super().__init__(repository)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        sort_by: str | None = None,
        sort_desc: bool = False,
        eager_load: list[str] | None = None,
    ):
        stmt = select(self._repository.model)
        from sqlalchemy.orm import selectinload
        for rel in ['id_publicacion']:
            if hasattr(self._repository.model, rel):
                stmt = stmt.options(selectinload(getattr(self._repository.model, rel)))
        if sort_by and sort_by in {'id_metricas_calidad_publi', 'id_publicacion', 'fecha_captura', 'cantidad_fotos', 'tiene_video', 'caracteristicas_completas', 'puntaje_calidad'}:
            order_col = getattr(self._repository.model, sort_by)
            stmt = stmt.order_by(order_col.desc() if sort_desc else order_col.asc())
        count_stmt = select(self._repository.model)
        result = await self._repository.db.execute(count_stmt)
        total = len(result.scalars().all())
        stmt = stmt.offset(skip).limit(limit)
        result = await self._repository.db.execute(stmt)
        items = list(result.scalars().all())
        return items, total


    async def get_by_id(self, id: int):
        item = await self._repository.get(id, eager_load=['id_publicacion'])
        if not item:
            from domain.exceptions import NotFoundException
            raise NotFoundException('Metricas_calidad_publicacion', id)
        return item