from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Any, Tuple, List

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: int) -> Optional[T]: ...

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[T], int]: ...

    @abstractmethod
    def create(self, **data) -> T: ...

    @abstractmethod
    def update(self, id: int, **data) -> Optional[T]: ...

    @abstractmethod
    def delete(self, id: int) -> Optional[T]: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def get_by_ids(self, ids: List[int]) -> List[T]: ...

    @abstractmethod
    def bulk_create(self, items: List[dict]) -> List[T]: ...

    @abstractmethod
    def bulk_update(self, ids: List[int], **data) -> int: ...
