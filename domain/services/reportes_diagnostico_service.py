from typing import Optional
from infrastructure.persistence.repositories.reportes_diagnostico import Reportes_diagnosticoRepository
from domain.services.base import BaseDomainService


class Reportes_diagnosticoService(BaseDomainService[Reportes_diagnosticoRepository, dict, dict]):

    def __init__(self, repository: Reportes_diagnosticoRepository):
        super().__init__(repository)
