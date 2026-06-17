from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.metricas_reputacion import Metricas_reputacion
from infrastructure.persistence.repositories.metricas_reputacion import Metricas_reputacionRepository
from application.services.base import BaseService
from application.dto.metricas_reputacion import Metricas_reputacionCreate, Metricas_reputacionUpdate


class Metricas_reputacionService(BaseService[Metricas_reputacionRepository, Metricas_reputacionCreate, Metricas_reputacionUpdate]):

    def __init__(self, repository: Metricas_reputacionRepository):
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
        if search:
            filters = [
                Metricas_reputacion.nivel_reputacion.ilike(f"%{search}%"),
                Metricas_reputacion.insignia.ilike(f"%{search}%")
            ]
            stmt = stmt.where(or_(*filters))
        if sort_by and sort_by in {'id_metricas_reputacion', 'id_vendedor', 'fecha_captura', 'ventas_totales_periodo', 'total_reclamos', 'total_mediaciones', 'total_canceladas', 'total_envios_incorrectos', 'nivel_reputacion', 'insignia'}:
            order_col = getattr(self._repository.model, sort_by)
            stmt = stmt.order_by(order_col.desc() if sort_desc else order_col.asc())
        count_stmt = select(self._repository.model)
        if search:
            count_stmt = count_stmt.where(or_(*filters))
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
            raise NotFoundException('Metricas_reputacion', id)
        return item