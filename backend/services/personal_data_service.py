from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.metrica_reputacion_model import Reputacion
from schemas import PersonalDataResponse


class UserNotFoundError(Exception):
    pass


def get_personal_data(db: Session, vendedor_id: int) -> PersonalDataResponse:

    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).first()

    if not vendedor:
        raise UserNotFoundError()

    insignia = None
    reputacion = db.query(Reputacion).filter(Reputacion.id_vendedor == vendedor_id).first()

    if reputacion:
        insignia = reputacion.insignia

    return PersonalDataResponse(
        nombre_tienda=vendedor.nombre_tienda,
        codigo_pais=vendedor.codigo_pais,
        tipo_plan=vendedor.tipo_plan,
        insignia=insignia,
    )
