from typing import Optional
from infrastructure.persistence.repositories.publicacion import PublicacionRepository
from domain.services.base import BaseDomainService


class PublicacionService(BaseDomainService[PublicacionRepository, dict, dict]):

    def __init__(self, repository: PublicacionRepository):
        super().__init__(repository)
