from typing import Optional
from infrastructure.persistence.repositories.moneda import MonedaRepository
from domain.services.base import BaseDomainService


class MonedaService(BaseDomainService[MonedaRepository, dict, dict]):

    def __init__(self, repository: MonedaRepository):
        super().__init__(repository)
