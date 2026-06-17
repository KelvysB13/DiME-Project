from typing import Optional
from infrastructure.persistence.repositories.rendimiento_publicacion import Rendimiento_publicacionRepository
from domain.services.base import BaseDomainService


class Rendimiento_publicacionService(BaseDomainService[Rendimiento_publicacionRepository, dict, dict]):

    def __init__(self, repository: Rendimiento_publicacionRepository):
        super().__init__(repository)
