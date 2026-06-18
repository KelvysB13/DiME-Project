from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import Mapped


class AuditMixin:
    created_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    created_by: Mapped[int | None] = Column(Integer, nullable=True)
    updated_by: Mapped[int | None] = Column(Integer, nullable=True)
