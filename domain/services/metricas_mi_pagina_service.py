from typing import Optional
from infrastructure.persistence.repositories.metricas_mi_pagina import Metricas_mi_paginaRepository
from domain.services.base import BaseDomainService


class Metricas_mi_paginaService(BaseDomainService[Metricas_mi_paginaRepository, dict, dict]):

    def __init__(self, repository: Metricas_mi_paginaRepository):
        super().__init__(repository)
