from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import Mapped
from resources.db import Base


class TimeStampedModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    disabled_at: Mapped[datetime] = Column(DateTime, nullable=True, default=None)
