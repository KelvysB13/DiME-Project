from typing import Generic, TypeVar, Optional, List
from domain.repositories.base import BaseRepository
from domain.exceptions import NotFoundException

R = TypeVar("R", bound=BaseRepository)
C = TypeVar("C")
U = TypeVar("U")


class BaseService(Generic[R, C, U]):
    def __init__(self, repository: R):
        self._repository = repository

    def get_by_id(self, id: int, eager_load: Optional[List[str]] = None):
        item = self._repository.get(id, eager_load=eager_load)
        if not item:
            raise NotFoundException(self._get_entity_name(), id)
        return item

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        eager_load: Optional[List[str]] = None,
    ):
        return self._repository.get_all(skip=skip, limit=limit, eager_load=eager_load)

    def create(self, data: C):
        return self._repository.create(**data.model_dump())

    def update(self, id: int, data: U):
        self.get_by_id(id)
        return self._repository.update(id, **data.model_dump(exclude_unset=True))

    def delete(self, id: int):
        item = self.get_by_id(id)
        return self._repository.delete(id)

    def _get_entity_name(self) -> str:
        return type(self).__name__.replace("Service", "")
