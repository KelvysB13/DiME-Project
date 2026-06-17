from sqlalchemy.orm import Session
from infrastructure.persistence.models.plan_saas import Plan_saas
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Plan_saasRepository(SQLAlchemyRepository[Plan_saas]):
    def __init__(self, db: Session):
        super().__init__(db, Plan_saas)
