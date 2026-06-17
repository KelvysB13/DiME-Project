from typing import Generic, TypeVar
from domain.repositories.base import BaseRepository
from domain.exceptions.base import NotFoundException

R = TypeVar("R", bound=BaseRepository)
C = TypeVar("C")
U = TypeVar("U")


class BaseDomainService(Generic[R, C, U]):
    def __init__(self, repository: R):
        self._repository = repository

    def get_by_id(self, id: int):
        item = self._repository.get(id)
        if not item:
            raise NotFoundException(self._get_entity_name(), id)
        return item

    def get_all(self, skip: int = 0, limit: int = 100):
        return self._repository.get_all(skip=skip, limit=limit)

    def create(self, **data):
        return self._repository.create(**data)

    def update(self, id: int, **data):
        self.get_by_id(id)
        return self._repository.update(id, **data)

    def delete(self, id: int):
        item = self.get_by_id(id)
        return self._repository.delete(id)

    def _get_entity_name(self) -> str:
        return type(self).__name__.replace("Service", "")
