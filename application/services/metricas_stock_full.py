from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.metricas_stock_full import Metricas_stock_full
from infrastructure.persistence.repositories.metricas_stock_full import Metricas_stock_fullRepository
from application.services.base import BaseService
from application.dto.metricas_stock_full import Metricas_stock_fullCreate, Metricas_stock_fullUpdate


class Metricas_stock_fullService(BaseService[Metricas_stock_fullRepository, Metricas_stock_fullCreate, Metricas_stock_fullUpdate]):

    def __init__(self, repository: Metricas_stock_fullRepository):
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
        for rel in ['id_vendedor']:
            if hasattr(self._repository.model, rel):
                stmt = stmt.options(selectinload(getattr(self._repository.model, rel)))
        if sort_by and sort_by in {'id_metricas_stock', 'id_vendedor', 'fecha_captura', 'espacios_p_asignados', 'espacios_g_asignados', 'puntaje_calidad', 'productos_no_aptos_venta', 'productos_sin_rotacion', 'productos_antiguedad', 'productos_exceso_proyeccion'}:
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
        item = await self._repository.get(id, eager_load=['id_vendedor'])
        if not item:
            from domain.exceptions import NotFoundException
            raise NotFoundException('Metricas_stock_full', id)
        return item