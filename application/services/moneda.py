from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.moneda import Moneda
from infrastructure.persistence.repositories.moneda import MonedaRepository
from application.services.base import BaseService
from application.dto.moneda import MonedaCreate, MonedaUpdate


class MonedaService(BaseService[MonedaRepository, MonedaCreate, MonedaUpdate]):

    def __init__(self, repository: MonedaRepository):
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
        if search:
            filters = [
                Moneda.codigo_moneda.ilike(f"%{search}%"),
                Moneda.nombre_moneda.ilike(f"%{search}%"),
                Moneda.simbolo.ilike(f"%{search}%")
            ]
            stmt = stmt.where(or_(*filters))
        if sort_by and sort_by in {'codigo_moneda', 'nombre_moneda', 'simbolo'}:
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