from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: int, eager_load: list[str] | None = None, include_deleted: bool = False) -> T | None: ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, eager_load: list[str] | None = None, include_deleted: bool = False) -> tuple[list[T], int]: ...

    @abstractmethod
    async def create(self, **data) -> T: ...

    @abstractmethod
    async def update(self, id: int, **data) -> T | None: ...

    @abstractmethod
    async def delete(self, id: int) -> T | None: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def get_by_ids(self, ids: list[int]) -> list[T]: ...

    @abstractmethod
    async def bulk_create(self, items: list[dict]) -> list[T]: ...

    @abstractmethod
    async def bulk_update(self, ids: list[int], **data) -> int: ...

    @abstractmethod
    async def soft_delete(self, id: int) -> T | None: ...

    @abstractmethod
    async def restore(self, id: int) -> T | None: ...
