from sqlalchemy.orm import Session
from infrastructure.persistence.models.rendimiento_publicacion import Rendimiento_publicacion
from infrastructure.persistence.repositories.base import SQLAlchemyRepository


class Rendimiento_publicacionRepository(SQLAlchemyRepository[Rendimiento_publicacion]):
    def __init__(self, db: Session):
        super().__init__(db, Rendimiento_publicacion)
