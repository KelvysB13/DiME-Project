from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from config.settings import DATABASE_URL, DB_POOL_SIZE, DB_MAX_OVERFLOW

_async_url = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
_async_url = _async_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    _async_url,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
