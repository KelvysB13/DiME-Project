from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.rendimiento_publicacion import Rendimiento_publicacion
from infrastructure.persistence.repositories.rendimiento_publicacion import Rendimiento_publicacionRepository
from application.services.base import BaseService
from application.dto.rendimiento_publicacion import Rendimiento_publicacionCreate, Rendimiento_publicacionUpdate


class Rendimiento_publicacionService(BaseService[Rendimiento_publicacionRepository, Rendimiento_publicacionCreate, Rendimiento_publicacionUpdate]):

    def __init__(self, repository: Rendimiento_publicacionRepository):
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
        if sort_by and sort_by in {'id_rendimiento_publi', 'id_publicacion', 'fecha_captura', 'fecha_inicio_periodo', 'fecha_fin_periodo', 'visitas', 'ventas'}:
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
            raise NotFoundException('Rendimiento_publicacion', id)
        return item