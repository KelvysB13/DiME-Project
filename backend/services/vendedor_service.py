from math import ceil
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.vendedor_model import Vendedor
from schemas.vendedor_schema import VendedorResponse, VendedorListResponse


class VendedorNotFoundError(Exception):
    pass


def list_vendedores(db: Session, page: int = 1, per_page: int = 15, search: str = "") -> VendedorListResponse:
    query = db.query(Vendedor)

    if search:
        like = f"%{search}%"
        query = query.filter(
            Vendedor.user_name.ilike(like)
            | Vendedor.nombre_tienda.ilike(like)
            | Vendedor.email.ilike(like)
        )

    total = query.with_entities(func.count(Vendedor.id_vendedor)).scalar()
    total_pages = max(1, ceil(total / per_page)) if total > 0 else 1

    offset = (page - 1) * per_page
    vendedores = (
        query.order_by(Vendedor.id_vendedor)
        .offset(offset)
        .limit(per_page)
        .all()
    )

    return VendedorListResponse(
        vendedores=[_vendedor_to_response(v) for v in vendedores],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )


def toggle_vendedor_status(db: Session, vendedor_id: int) -> VendedorResponse:
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).first()
    if not vendedor:
        raise VendedorNotFoundError()
    vendedor.esta_activo = not vendedor.esta_activo
    db.commit()
    db.refresh(vendedor)
    return _vendedor_to_response(vendedor)


def delete_vendedor(db: Session, vendedor_id: int) -> None:
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).first()
    if not vendedor:
        raise VendedorNotFoundError()

    from models.publicacion_model import Publicacion
    from models.metrica_reputacion_model import Reputacion
    from models.metrica_negocio_model import Negocio
    from models.metrica_costo_model import Costo
    from models.metrica_stock_model import Stock
    from models.metrica_pagina_model import Pagina
    from models.rendimiento_model import Rendimiento
    from models.metrica_calidad_model import Calidad
    from models.reporte_model import Reporte

    publicacion_ids = [
        pid for (pid,) in db.query(Publicacion.id_publicacion)
        .filter(Publicacion.id_vendedor == vendedor_id)
        .all()
    ]

    if publicacion_ids:
        db.query(Calidad).filter(Calidad.id_publicacion.in_(publicacion_ids)).delete(synchronize_session=False)
        db.query(Rendimiento).filter(Rendimiento.id_publicacion.in_(publicacion_ids)).delete(synchronize_session=False)

    db.query(Publicacion).filter(Publicacion.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Reporte).filter(Reporte.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Reputacion).filter(Reputacion.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Negocio).filter(Negocio.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Costo).filter(Costo.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Stock).filter(Stock.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Pagina).filter(Pagina.id_vendedor == vendedor_id).delete(synchronize_session=False)
    db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).delete(synchronize_session=False)

    db.commit()


def _vendedor_to_response(v: Vendedor) -> VendedorResponse:
    return VendedorResponse(
        id_vendedor=v.id_vendedor,
        user_name=v.user_name,
        nombre_tienda=v.nombre_tienda,
        codigo_pais=v.codigo_pais,
        moneda_local=v.moneda_local,
        tipo_plan=v.tipo_plan,
        email=v.email,
        esta_activo=v.esta_activo,
        fecha_creacion=v.fecha_creacion,
    )
