from sqlalchemy.orm import Session
from models.plan_model import Plan
from schemas.plan_schema import PlanResponse

def get_planes(db: Session) -> list[PlanResponse]:
    planes = db.query(Plan).filter(Plan.id != 1).order_by(Plan.id).all()
    return [
        PlanResponse(
            id=p.id,
            nombre_plan=p.nombre_plan,
            precio_mensual=float(p.precio_mensual),
            limite_publicaciones=p.limite_publicaciones,
            limite_metricas_dias=p.limite_metricas_dias,
            features=p.features,
            descripcion=p.descripcion,
        )
        for p in planes
    ]
