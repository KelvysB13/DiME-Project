from typing import Optional
from infrastructure.persistence.repositories.metricas_negocio import Metricas_negocioRepository
from domain.services.base import BaseDomainService


class Metricas_negocioService(BaseDomainService[Metricas_negocioRepository, dict, dict]):

    def __init__(self, repository: Metricas_negocioRepository):
        super().__init__(repository)
