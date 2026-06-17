from typing import Optional
from infrastructure.persistence.repositories.plan_saas import Plan_saasRepository
from domain.services.base import BaseDomainService


class Plan_saasService(BaseDomainService[Plan_saasRepository, dict, dict]):

    def __init__(self, repository: Plan_saasRepository):
        super().__init__(repository)
