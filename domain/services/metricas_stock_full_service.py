from typing import Optional
from infrastructure.persistence.repositories.metricas_stock_full import Metricas_stock_fullRepository
from domain.services.base import BaseDomainService


class Metricas_stock_fullService(BaseDomainService[Metricas_stock_fullRepository, dict, dict]):

    def __init__(self, repository: Metricas_stock_fullRepository):
        super().__init__(repository)
