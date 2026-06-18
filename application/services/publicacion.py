from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from infrastructure.persistence.models.publicacion import Publicacion
from infrastructure.persistence.repositories.publicacion import PublicacionRepository
from application.services.base import BaseService
from application.dto.publicacion import PublicacionCreate, PublicacionUpdate


class PublicacionService(BaseService[PublicacionRepository, PublicacionCreate, PublicacionUpdate]):

    def __init__(self, repository: PublicacionRepository):
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
        if search:
            filters = [
                Publicacion.ml_item_id.ilike(f"%{search}%"),
                Publicacion.titulo.ilike(f"%{search}%"),
                Publicacion.tipo_publicacion.ilike(f"%{search}%"),
                Publicacion.estado_publicacion.ilike(f"%{search}%")
            ]
            stmt = stmt.where(or_(*filters))
        if sort_by and sort_by in {'id_publicacion', 'id_vendedor', 'ml_item_id', 'titulo', 'tipo_publicacion', 'estado_publicacion'}:
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
            raise NotFoundException('Publicacion', id)
        return item