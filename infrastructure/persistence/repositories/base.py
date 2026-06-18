from typing import Generic, TypeVar
from sqlalchemy import select, func, update as sa_update, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from domain.repositories.base import BaseRepository

T = TypeVar("T")


class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
    def __init__(self, db: AsyncSession, model: type[T]):
        self.db = db
        self.model = model
        self.pk_name = inspect(model).primary_key[0].name
        self._relationships = [
            r.key for r in inspect(model).relationships
        ]

    def _apply_soft_delete_filter(self, stmt):
        if hasattr(self.model, "deleted_at"):
            return stmt.where(self.model.deleted_at.is_(None))
        if hasattr(self.model, "is_deleted"):
            return stmt.where(self.model.is_deleted == False)
        if hasattr(self.model, "activo"):
            return stmt.where(self.model.activo == True)
        return stmt

    def _apply_eager_load(self, stmt, eager_load: list[str] | None = None):
        if eager_load:
            for rel in eager_load:
                if rel in self._relationships:
                    stmt = stmt.options(selectinload(getattr(self.model, rel)))
        return stmt

    async def get(self, id: int, eager_load: list[str] | None = None, include_deleted: bool = False) -> T | None:
        stmt = select(self.model)
        if not include_deleted:
            stmt = self._apply_soft_delete_filter(stmt)
        stmt = self._apply_eager_load(stmt, eager_load)
        stmt = stmt.where(getattr(self.model, self.pk_name) == id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        eager_load: list[str] | None = None,
        include_deleted: bool = False,
    ) -> tuple[list[T], int]:
        stmt = select(self.model)
        if not include_deleted:
            stmt = self._apply_soft_delete_filter(stmt)
        stmt = self._apply_eager_load(stmt, eager_load)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        items = list(result.scalars().all())
        return items, total

    async def create(self, **data) -> T:
        db_item = self.model(**data)
        self.db.add(db_item)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def update(self, id: int, **data) -> T | None:
        db_item = await self.get(id)
        if not db_item:
            return None
        for key, value in data.items():
            setattr(db_item, key, value)
        await self.db.commit()
        await self.db.refresh(db_item)
        return db_item

    async def delete(self, id: int) -> T | None:
        db_item = await self.get(id)
        if db_item:
            await self.db.delete(db_item)
            await self.db.commit()
        return db_item

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_soft_delete_filter(stmt)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_by_ids(self, ids: list[int]) -> list[T]:
        if not ids:
            return []
        pk = getattr(self.model, self.pk_name)
        stmt = select(self.model).where(pk.in_(ids))
        stmt = self._apply_soft_delete_filter(stmt)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def bulk_create(self, items: list[dict]) -> list[T]:
        if not items:
            return []
        db_items = [self.model(**item) for item in items]
        self.db.add_all(db_items)
        await self.db.commit()
        for item in db_items:
            await self.db.refresh(item)
        return db_items

    async def bulk_update(self, ids: list[int], **data) -> int:
        if not ids:
            return 0
        pk = getattr(self.model, self.pk_name)
        result = await self.db.execute(
            sa_update(self.model)
            .where(pk.in_(ids))
            .values(**data)
        )
        await self.db.commit()
        return result.rowcount

    async def soft_delete(self, id: int) -> T | None:
        item = await self.get(id)
        if item and hasattr(item, "soft_delete"):
            item.soft_delete()
            await self.db.commit()
        return item

    async def restore(self, id: int) -> T | None:
        item = await self.get(id, include_deleted=True)
        if item and hasattr(item, "restore"):
            item.restore()
            await self.db.commit()
        return item

    async def get_deleted(self, skip: int = 0, limit: int = 100) -> tuple[list[T], int]:
        stmt = select(self.model)
        if hasattr(self.model, "deleted_at"):
            stmt = stmt.where(self.model.deleted_at.isnot(None))
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar()
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        items = list(result.scalars().all())
        return items, total
