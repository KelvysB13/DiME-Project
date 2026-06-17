from typing import Optional
from infrastructure.persistence.repositories.vendedor import VendedorRepository
from domain.services.base import BaseDomainService


class VendedorService(BaseDomainService[VendedorRepository, dict, dict]):

    def __init__(self, repository: VendedorRepository):
        super().__init__(repository)
