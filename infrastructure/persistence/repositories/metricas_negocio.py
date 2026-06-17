from sqlalchemy.orm import Session
from infrastructure.persistence.models.metricas_negocio import Metricas_negocio
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Metricas_negocioRepository(SQLAlchemyRepository[Metricas_negocio]):
    def __init__(self, db: Session):
        super().__init__(db, Metricas_negocio)
