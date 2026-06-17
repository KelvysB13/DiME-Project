from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped
from typing import Optional


class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = Column(DateTime, nullable=True, default=None)

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self) -> None:
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
