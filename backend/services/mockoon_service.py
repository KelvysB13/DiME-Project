from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.vendedor_model import Vendedor
from models.metrica_reputacion_model import Reputacion
from models.metrica_negocio_model import Negocio
from models.metrica_costo_model import Costo
from models.metrica_stock_model import Stock
from schemas.mockoon_schema import MetricsRequest

PLAN_MAP = {
    "básico": 1,
    "plan básico": 1,
    "premium": 2,
    "plan premium": 2,
}


def save_metrics(db: Session, data: MetricsRequest) -> dict:
    basicos = data.datos_basicos
    negocio = data.metrica_negocio
    costo = data.metrica_costo
    reputacion = data.metrica_reputacion
    stock_full = data.metrica_stock_full

    plan_recibido = str(basicos.tipo_plan).lower().strip()
    tipo_plan_id = PLAN_MAP.get(plan_recibido, 1)

    filters = [Vendedor.user_name == basicos.user_name]
    if basicos.email:
        filters.append(Vendedor.email == basicos.email)

    vendedor = db.query(Vendedor).filter(or_(*filters)).first()
    if vendedor:
        vendedor.user_name = basicos.user_name
        vendedor.nombre_tienda = basicos.nombre_tienda
        vendedor.tipo_plan = tipo_plan_id
        if basicos.email:
            vendedor.email = basicos.email
    else:
        vendedor = Vendedor(
            user_name=basicos.user_name,
            nombre_tienda=basicos.nombre_tienda,
            codigo_pais=basicos.codigo_pais,
            moneda_local=basicos.moneda_local,
            tipo_plan=tipo_plan_id,
            email=basicos.email or f"{basicos.user_name}@test-dime.com",
            password="mockoon_placeholder",
            esta_activo=True,
        )
        db.add(vendedor)
    db.flush()

    id_vendedor = vendedor.id_vendedor

    rep = db.query(Reputacion).filter(Reputacion.id_vendedor == id_vendedor).first()
    if rep:
        rep.total_reclamos = reputacion.total_reclamos
        rep.nivel_reputacion = reputacion.nivel_reputacion
        rep.insignia = reputacion.insignia
    else:
        rep = Reputacion(
            id_vendedor=id_vendedor,
            ventas_totales_periodo=negocio.ventas_totales_periodo,
            total_reclamos=reputacion.total_reclamos,
            total_mediaciones=reputacion.total_mediaciones,
            total_canceladas=reputacion.total_canceladas,
            total_envios_incorrectos=reputacion.total_envios_incorrectos,
            nivel_reputacion=reputacion.nivel_reputacion,
            insignia=reputacion.insignia,
        )
        db.add(rep)

    neg = db.query(Negocio).filter(Negocio.id_vendedor == id_vendedor).first()
    if neg:
        neg.ventas_brutas_moneda_local = negocio.ventas_brutas_moneda_local
        neg.visitas_totales = negocio.visitas_totales
    else:
        neg = Negocio(
            id_vendedor=id_vendedor,
            fecha_inicio_periodo=negocio.fecha_inicio_periodo,
            fecha_fin_periodo=negocio.fecha_final_periodo,
            ventas_brutas_moneda_local=negocio.ventas_brutas_moneda_local,
            ventas_brutas_usd=negocio.ventas_brutas_usd,
            unidades_vendidas=negocio.unidades_vendidas,
            visitas_totales=negocio.visitas_totales,
            intencion_compra=negocio.intencion_compra,
            ventas_concretadas=negocio.ventas_concretadas,
            precio_promedio_unidad=negocio.precio_promedio_unidad,
            precio_promedio_venta=negocio.precio_promedio_venta,
        )
        db.add(neg)

    cos = db.query(Costo).filter(Costo.id_vendedor == id_vendedor).first()
    if cos:
        cos.neto_recibido = costo.neto_recibido
    else:
        cos = Costo(
            id_vendedor=id_vendedor,
            ventas_cobradas_total=costo.ventas_cobradas_total,
            neto_recibido=costo.neto_recibido,
            cargos_por_venta=costo.cargos_por_venta,
            costos_envio=costo.costos_envio,
            inversion_ads=costo.inversion_ads,
            otros_cargos=costo.otros_cargos,
            cargos_envio_full=costo.cargos_envio_full,
            descuento_reputacion=costo.descuento_reputacion,
        )
        db.add(cos)

    stk = db.query(Stock).filter(Stock.id_vendedor == id_vendedor).first()
    if stk:
        stk.puntaje_calidad = stock_full.puntaje_calidad
    else:
        stk = Stock(
            id_vendedor=id_vendedor,
            espacios_p_asignados=stock_full.espacios_p_asignados,
            espacios_g_asignados=stock_full.espacios_g_asignados,
            puntaje_calidad=stock_full.puntaje_calidad,
            productos_no_aptos_venta=stock_full.productos_no_aptos_venta,
            productos_sin_rotacion=stock_full.productos_sin_rotacion,
            productos_antiguedad=stock_full.productos_antiguedad,
            productos_exceso_proyeccion=stock_full.productos_exceso_proyeccion,
        )
        db.add(stk)

    db.commit()

    return {"status": "success", "message": "Datos inyectados perfectamente en Postgres"}
