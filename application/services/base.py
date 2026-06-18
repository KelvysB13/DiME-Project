from typing import Generic, TypeVar
from domain.repositories.base import BaseRepository
from domain.exceptions import NotFoundException

R = TypeVar("R", bound=BaseRepository)
C = TypeVar("C")
U = TypeVar("U")


class BaseService(Generic[R, C, U]):
    def __init__(self, repository: R):
        self._repository = repository

    async def get_by_id(self, id: int, eager_load: list[str] | None = None):
        item = await self._repository.get(id, eager_load=eager_load)
        if not item:
            raise NotFoundException(self._get_entity_name(), id)
        return item

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        eager_load: list[str] | None = None,
    ):
        return await self._repository.get_all(skip=skip, limit=limit, eager_load=eager_load)

    async def create(self, data: C):
        return await self._repository.create(**data.model_dump())

    async def update(self, id: int, data: U):
        await self.get_by_id(id)
        return await self._repository.update(id, **data.model_dump(exclude_unset=True))

    async def delete(self, id: int):
        await self.get_by_id(id)
        return await self._repository.delete(id)

    async def soft_delete(self, id: int):
        return await self._repository.soft_delete(id)

    async def restore(self, id: int):
        return await self._repository.restore(id)

    def _get_entity_name(self) -> str:
        return type(self).__name__.replace("Service", "")
