from typing import Optional
from infrastructure.persistence.repositories.metricas_reputacion import Metricas_reputacionRepository
from domain.services.base import BaseDomainService


class Metricas_reputacionService(BaseDomainService[Metricas_reputacionRepository, dict, dict]):

    def __init__(self, repository: Metricas_reputacionRepository):
        super().__init__(repository)
