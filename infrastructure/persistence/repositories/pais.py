from sqlalchemy.orm import Session
from infrastructure.persistence.models.pais import Pais
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class PaisRepository(SQLAlchemyRepository[Pais]):
    def __init__(self, db: Session):
        super().__init__(db, Pais)
