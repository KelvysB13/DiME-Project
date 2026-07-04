from sqlalchemy import text
from sqlalchemy.orm import Session

from models.vendedor_model import Vendedor
from models.publicacion_model import Publicacion
from models.reporte_model import Reporte
from models.metrica_reputacion_model import Reputacion
from models.metrica_negocio_model import Negocio
from models.metrica_costo_model import Costo
from models.metrica_stock_model import Stock
from models.metrica_pagina_model import Pagina
from models.rendimiento_model import Rendimiento
from models.metrica_calidad_model import Calidad


class AccountDeletionError(Exception):
    pass


def delete_account(db: Session, vendedor_id: int) -> None:
    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).first()
    if not vendedor:
        raise AccountDeletionError("Vendedor no encontrado")

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

    db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_diagnostico_reputacion"))
    db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_diagnostico_finanzas"))
    db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_diagnostico_publicaciones"))
    db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_diagnostico_ads"))
    db.execute(text("REFRESH MATERIALIZED VIEW CONCURRENTLY mv_diagnostico_stock"))

    db.commit()
