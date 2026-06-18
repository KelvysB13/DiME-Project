from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.persistence.models.plan_saas import Plan_saas
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Plan_saasRepository(SQLAlchemyRepository[Plan_saas]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Plan_saas)
