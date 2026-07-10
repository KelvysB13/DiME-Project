from sqlalchemy.orm import Session
from models.plan_model import Plan
from schemas.plan_schema import PlanCreate, PlanUpdate, PlanResponse

class PlanNotFoundError(Exception):
    pass

class PlanNameAlreadyExistsError(Exception):
    pass

def obtener_plans(db: Session) -> list[PlanResponse]:
    planes = db.query(Plan).order_by(Plan.id).all()
    return [_plan_to_response(p) for p in planes]


def obtener_plan_por_id(db: Session, plan_id: int) -> PlanResponse:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise PlanNotFoundError()
    return _plan_to_response(plan)


def crear_plan(db: Session, payload: PlanCreate) -> PlanResponse:
    existing = db.query(Plan).filter(Plan.nombre_plan == payload.nombre_plan).first()
    if existing:
        raise PlanNameAlreadyExistsError()

    max_id = db.query(Plan.id).order_by(Plan.id.desc()).first()
    new_id = (max_id[0] + 1) if max_id else 1

    plan = Plan(
        id=new_id,
        nombre_plan=payload.nombre_plan,
        precio_mensual=payload.precio_mensual,
        limite_publicaciones=payload.limite_publicaciones,
        limite_metricas_dias=payload.limite_metricas_dias,
        features=payload.features,
        descripcion=payload.descripcion,
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)
    return _plan_to_response(plan)


def actualizar_plan(db: Session, plan_id: int, payload: PlanUpdate) -> PlanResponse:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise PlanNotFoundError()

    if payload.nombre_plan is not None:
        duplicate = db.query(Plan).filter(
            Plan.nombre_plan == payload.nombre_plan,
            Plan.id != plan_id
        ).first()
        if duplicate:
            raise PlanNameAlreadyExistsError()
        plan.nombre_plan = payload.nombre_plan

    if payload.precio_mensual is not None:
        plan.precio_mensual = payload.precio_mensual
    if payload.limite_publicaciones is not None:
        plan.limite_publicaciones = payload.limite_publicaciones
    if payload.limite_metricas_dias is not None:
        plan.limite_metricas_dias = payload.limite_metricas_dias
    if payload.features is not None:
        plan.features = payload.features
    if payload.descripcion is not None:
        plan.descripcion = payload.descripcion

    db.commit()
    db.refresh(plan)
    return _plan_to_response(plan)


def eliminar_plan(db: Session, plan_id: int) -> None:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise PlanNotFoundError()
    db.delete(plan)
    db.commit()


def _plan_to_response(plan: Plan) -> PlanResponse:
    return PlanResponse(
        id=plan.id,
        nombre_plan=plan.nombre_plan,
        precio_mensual=float(plan.precio_mensual),
        limite_publicaciones=plan.limite_publicaciones,
        limite_metricas_dias=plan.limite_metricas_dias,
        features=plan.features,
        descripcion=plan.descripcion,
    )
