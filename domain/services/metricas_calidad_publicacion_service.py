from typing import Optional
from infrastructure.persistence.repositories.metricas_calidad_publicacion import Metricas_calidad_publicacionRepository
from domain.services.base import BaseDomainService


class Metricas_calidad_publicacionService(BaseDomainService[Metricas_calidad_publicacionRepository, dict, dict]):

    def __init__(self, repository: Metricas_calidad_publicacionRepository):
        super().__init__(repository)
