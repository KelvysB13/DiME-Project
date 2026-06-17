from typing import Generic, TypeVar, Optional, Any, List, Tuple, Dict, Type
from sqlalchemy import inspect, update as sa_update
from sqlalchemy.orm import Session, joinedload, selectinload
from domain.repositories.base import BaseRepository

T = TypeVar("T")


class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
        self.pk_name = inspect(model).primary_key[0].name
        self._relationships = [
            r.key for r in inspect(model).relationships
        ]

    def _apply_soft_delete_filter(self, query):
        if hasattr(self.model, "deleted_at"):
            return query.filter(self.model.deleted_at.is_(None))
        if hasattr(self.model, "is_deleted"):
            return query.filter(self.model.is_deleted == False)
        if hasattr(self.model, "activo"):
            return query.filter(self.model.activo == True)
        return query

    def get(self, id: int, eager_load: Optional[List[str]] = None, include_deleted: bool = False) -> Optional[T]:
        query = self.db.query(self.model)
        if not include_deleted:
            query = self._apply_soft_delete_filter(query)
        if eager_load:
            for rel in eager_load:
                if rel in self._relationships:
                    query = query.options(selectinload(getattr(self.model, rel)))
        return query.filter(getattr(self.model, self.pk_name) == id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        eager_load: Optional[List[str]] = None,
        include_deleted: bool = False,
    ) -> Tuple[List[T], int]:
        query = self.db.query(self.model)
        if not include_deleted:
            query = self._apply_soft_delete_filter(query)
        if eager_load:
            for rel in eager_load:
                if rel in self._relationships:
                    query = query.options(selectinload(getattr(self.model, rel)))
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    def create(self, **data) -> T:
        db_item = self.model(**data)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, id: int, **data) -> Optional[T]:
        db_item = self.get(id)
        if not db_item:
            return None
        for key, value in data.items():
            setattr(db_item, key, value)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, id: int) -> Optional[T]:
        db_item = self.get(id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
        return db_item

    def count(self) -> int:
        query = self._apply_soft_delete_filter(self.db.query(self.model))
        return query.count()

    def get_by_ids(self, ids: List[int]) -> List[T]:
        if not ids:
            return []
        pk = getattr(self.model, self.pk_name)
        query = self._apply_soft_delete_filter(self.db.query(self.model))
        return query.filter(pk.in_(ids)).all()

    def bulk_create(self, items: List[dict]) -> List[T]:
        if not items:
            return []
        db_items = [self.model(**item) for item in items]
        self.db.add_all(db_items)
        self.db.commit()
        for item in db_items:
            self.db.refresh(item)
        return db_items

    def bulk_update(self, ids: List[int], **data) -> int:
        if not ids:
            return 0
        pk = getattr(self.model, self.pk_name)
        result = self.db.execute(
            sa_update(self.model)
            .where(pk.in_(ids))
            .values(**data)
        )
        self.db.commit()
        return result.rowcount

    def soft_delete(self, id: int) -> Optional[T]:
        item = self.get(id)
        if item and hasattr(item, "soft_delete"):
            item.soft_delete()
            self.db.commit()
        return item

    def restore(self, id: int) -> Optional[T]:
        item = self.get(id, include_deleted=True)
        if item and hasattr(item, "restore"):
            item.restore()
            self.db.commit()
        return item

    def get_deleted(self, skip: int = 0, limit: int = 100) -> Tuple[List[T], int]:
        query = self.db.query(self.model)
        if hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.isnot(None))
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
