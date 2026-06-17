from sqlalchemy.orm import Session
from infrastructure.persistence.models.moneda import Moneda
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class MonedaRepository(SQLAlchemyRepository[Moneda]):
    def __init__(self, db: Session):
        super().__init__(db, Moneda)
