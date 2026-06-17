from typing import Optional
from infrastructure.persistence.repositories.pais import PaisRepository
from domain.services.base import BaseDomainService


class PaisService(BaseDomainService[PaisRepository, dict, dict]):

    def __init__(self, repository: PaisRepository):
        super().__init__(repository)
