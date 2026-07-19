from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.plan_model import Plan


class PlanNotFoundError(Exception):
    pass


def change_plan(db: Session, vendedor_id: int, new_plan_id: int) -> None:
    plan = db.query(Plan).filter(Plan.id == new_plan_id).first()
    if not plan:
        raise PlanNotFoundError("Plan no encontrado")

    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).first()
    if not vendedor:
        raise PlanNotFoundError("Vendedor no encontrado")

    vendedor.tipo_plan = new_plan_id
    db.commit()
