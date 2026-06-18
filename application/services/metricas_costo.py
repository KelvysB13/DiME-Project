from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.metricas_costo import Metricas_costo
from infrastructure.persistence.repositories.metricas_costo import Metricas_costoRepository
from application.services.base import BaseService
from application.dto.metricas_costo import Metricas_costoCreate, Metricas_costoUpdate


class Metricas_costoService(BaseService[Metricas_costoRepository, Metricas_costoCreate, Metricas_costoUpdate]):

    def __init__(self, repository: Metricas_costoRepository):
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
        if sort_by and sort_by in {'id_metricas_costo', 'id_vendedor', 'fecha_captura', 'ventas_cobradas_total', 'neto_recibido', 'cargos_por_venta', 'costos_envio', 'inversion_ads', 'otros_cargos', 'cargos_envio_full', 'descuento_reputacion'}:
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
            raise NotFoundException('Metricas_costo', id)
        return item