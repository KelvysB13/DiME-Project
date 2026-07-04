from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.metrica_reputacion_model import Reputacion
from models.metrica_negocio_model import Negocio
from models.metrica_costo_model import Costo
from models.metrica_stock_model import Stock
from models.metrica_pagina_model import Pagina
from models.publicacion_model import Publicacion
from models.rendimiento_model import Rendimiento
from models.metrica_calidad_model import Calidad
from schemas import (DashboardResponse, ReputacionInfo, NegocioInfo, CostoInfo, StockInfo, PaginaInfo, PublicacionResumen)

def get_dashboard(db: Session, vendedor_id: int) -> DashboardResponse:

    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == vendedor_id).first()

    reputacion_info = None
    reputacion = db.query(Reputacion).filter(Reputacion.id_vendedor == vendedor_id).first()

    if reputacion:

        tasa_reclamos = (

            (reputacion.total_reclamos / reputacion.ventas_totales_periodo * 100)
            if reputacion.ventas_totales_periodo > 0 else 0.0
        )

        reputacion_info = ReputacionInfo(

            nivel=reputacion.nivel_reputacion,
            insignia=reputacion.insignia,
            ventas_totales=reputacion.ventas_totales_periodo,
            total_reclamos=reputacion.total_reclamos,
            total_mediaciones=reputacion.total_mediaciones,
            total_canceladas=reputacion.total_canceladas,
            tasa_reclamos=round(tasa_reclamos, 2),
        )

    negocio_info = None
    negocio = db.query(Negocio).filter(Negocio.id_vendedor == vendedor_id).first()

    if negocio:

        negocio_info = NegocioInfo(

            ventas_brutas_moneda_local=float(negocio.ventas_brutas_moneda_local),
            unidades_vendidas=negocio.unidades_vendidas,
            visitas_totales=negocio.visitas_totales,
            intencion_compra=negocio.intencion_compra,
            ventas_concretadas=negocio.ventas_concretadas,
        )

    costo_info = None
    costo = db.query(Costo).filter(Costo.id_vendedor == vendedor_id).first()

    if costo:

        costo_info = CostoInfo(

            ventas_cobradas_total=float(costo.ventas_cobradas_total),
            neto_recibido=float(costo.neto_recibido),
            cargos_por_venta=float(costo.cargos_por_venta),
            costos_envio=float(costo.costos_envio),
            inversion_ads=float(costo.inversion_ads),
        )

    stock_info = None
    stock = db.query(Stock).filter(Stock.id_vendedor == vendedor_id).first()

    if stock:

        stock_info = StockInfo(

            espacios_p_asignados=stock.espacios_p_asignados,
            puntaje_calidad=stock.puntaje_calidad,
            productos_no_aptos_venta=stock.productos_no_aptos_venta,
            productos_sin_rotacion=stock.productos_sin_rotacion,
        )

    pagina_info = None
    pagina = db.query(Pagina).filter(Pagina.id_vendedor == vendedor_id).first()

    if pagina:

        pagina_info = PaginaInfo(

            tiene_banner=pagina.tiene_banner,
            tiene_logo=pagina.tiene_logo,
            tiene_carruseles=pagina.tiene_carruseles,
            categorias_organizadas=pagina.categorias_organizadas,
        )

    publicaciones = db.query(Publicacion).filter(Publicacion.id_vendedor == vendedor_id).all()
    publicaciones_data = []

    for pub in publicaciones:

        rend = db.query(Rendimiento).filter(Rendimiento.id_publicacion == pub.id_publicacion).first()
        cal = db.query(Calidad).filter(Calidad.id_publicacion == pub.id_publicacion).first()
        visitas = rend.visitas if rend else 0
        ventas = rend.ventas if rend else 0

        publicaciones_data.append(PublicacionResumen(

            ml_item_id=pub.ml_item_id,
            titulo=pub.titulo,
            tipo_publicacion=pub.tipo_publicacion,
            estado_publicacion=pub.estado_publicacion,
            visitas=visitas,
            ventas=ventas,
            puntaje_calidad=cal.puntaje_calidad if cal else 0,
        ))

    return DashboardResponse(

        nombre_tienda=vendedor.nombre_tienda,
        codigo_pais=vendedor.codigo_pais,
        tipo_plan=vendedor.tipo_plan,
        reputacion=reputacion_info,
        negocio=negocio_info,
        costos=costo_info,
        stock=stock_info,
        pagina=pagina_info,
        publicaciones=publicaciones_data,
    )
