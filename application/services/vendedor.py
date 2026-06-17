from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.vendedor import Vendedor
from infrastructure.persistence.repositories.vendedor import VendedorRepository
from application.services.base import BaseService
from application.dto.vendedor import VendedorCreate, VendedorUpdate


class VendedorService(BaseService[VendedorRepository, VendedorCreate, VendedorUpdate]):

    def __init__(self, repository: VendedorRepository):
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
        for rel in ['codigo_pais', 'moneda_local', 'tipo_plan']:
            if hasattr(self._repository.model, rel):
                stmt = stmt.options(selectinload(getattr(self._repository.model, rel)))
        if search:
            filters = [
                Vendedor.user_name.ilike(f"%{search}%"),
                Vendedor.nombre_tienda.ilike(f"%{search}%"),
                Vendedor.codigo_pais.ilike(f"%{search}%"),
                Vendedor.moneda_local.ilike(f"%{search}%"),
                Vendedor.email.ilike(f"%{search}%"),
                Vendedor.access_token.ilike(f"%{search}%"),
                Vendedor.refresh_token.ilike(f"%{search}%")
            ]
            stmt = stmt.where(or_(*filters))
        if sort_by and sort_by in {'id_vendedor', 'user_name', 'nombre_tienda', 'codigo_pais', 'moneda_local', 'tipo_plan', 'email', 'access_token', 'refresh_token', 'tiempo_token', 'esta_activo', 'fecha_creacion'}:
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
        item = await self._repository.get(id, eager_load=['codigo_pais', 'moneda_local', 'tipo_plan'])
        if not item:
            from domain.exceptions import NotFoundException
            raise NotFoundException('Vendedor', id)
        return item