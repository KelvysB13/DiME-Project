from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.metricas_negocio import Metricas_negocio
from infrastructure.persistence.repositories.metricas_negocio import Metricas_negocioRepository
from application.services.base import BaseService
from application.dto.metricas_negocio import Metricas_negocioCreate, Metricas_negocioUpdate


class Metricas_negocioService(BaseService[Metricas_negocioRepository, Metricas_negocioCreate, Metricas_negocioUpdate]):

    def __init__(self, repository: Metricas_negocioRepository):
        super().__init__(repository)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
        eager_load: Optional[List[str]] = None,
    ):
        stmt = select(self._repository.model)
        from sqlalchemy.orm import selectinload
        for rel in ['id_vendedor']:
            if hasattr(self._repository.model, rel):
                stmt = stmt.options(selectinload(getattr(self._repository.model, rel)))
        if sort_by and sort_by in {'id_metricas_negocio', 'id_vendedor', 'fecha_captura', 'fecha_inicio_periodo', 'fecha_fin_periodo', 'ventas_brutas_moneda_local', 'ventas_brutas_usd', 'unidades_vendidas', 'visitas_totales', 'intencion_compra', 'ventas_concretadas', 'precio_promedio_unidad', 'precio_promedio_venta'}:
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
            raise NotFoundException('Metricas_negocio', id)
        return item