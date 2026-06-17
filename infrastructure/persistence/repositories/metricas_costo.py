from sqlalchemy.orm import Session
from infrastructure.persistence.models.metricas_costo import Metricas_costo
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_costoRepository(SQLAlchemyRepository[Metricas_costo]):
    def __init__(self, db: Session):
        super().__init__(db, Metricas_costo)
