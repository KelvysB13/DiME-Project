from typing import Optional
from infrastructure.persistence.repositories.metricas_costo import Metricas_costoRepository
from domain.services.base import BaseDomainService


class Metricas_costoService(BaseDomainService[Metricas_costoRepository, dict, dict]):

    def __init__(self, repository: Metricas_costoRepository):
        super().__init__(repository)
