from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.pais_model import Pais
from schemas import UserInfo


class UserNotFoundError(Exception):
    pass


def get_user_info(db: Session, vendedor_id: int) -> UserInfo:
    result = (
        db.query(Vendedor, Pais.nombre_pais)
        .join(Pais, Vendedor.codigo_pais == Pais.codigo_pais)
        .filter(Vendedor.id_vendedor == vendedor_id)
        .first()
    )

    if not result:
        raise UserNotFoundError()

    vendedor, nombre_pais = result

    return UserInfo(
        user_name=vendedor.user_name,
        nombre_tienda=vendedor.nombre_tienda,
        email=vendedor.email,
        nombre_pais=nombre_pais,
        es_admin=vendedor.es_admin,
    )
