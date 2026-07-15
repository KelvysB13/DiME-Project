import json
import logging
from datetime import date, timedelta
import jwt
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.checkout_schema import CheckoutRequest, CheckoutResponse
from models.tarjeta_model import Tarjeta
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from models.plan_model import Plan
from auth.hash_handler import hash_data
from auth.jwt_handler import ALGORITHM
from core.config import settings

logger = logging.getLogger(__name__)


class CheckoutError(Exception):
    pass


def _validate_luhn(card_number: str) -> bool:
    digits = [int(d) for d in card_number if d.isdigit()]
    if len(digits) != 16:
        return False
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return sum(digits) % 10 == 0


def _detect_card_type(card_number: str) -> str:
    if card_number.startswith("4"):
        return "Visa"
    if card_number.startswith("5"):
        return "MasterCard"
    raise CheckoutError("Tipo de tarjeta no soportado. Solo se aceptan Visa y MasterCard.")


def _build_expiry_date(month: int, year: int) -> date:
    year_full = 2000 + year
    expiry = date(year_full, month, 1)
    today = date.today()
    if expiry <= date(today.year, today.month, 1):
        raise CheckoutError("La tarjeta está vencida.")
    return expiry


def _decode_pre_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.app_secret_key, algorithms=[ALGORITHM])
        if payload.get("type") != "pre_register":
            raise CheckoutError("Token inválido.")
        return payload
    except jwt.ExpiredSignatureError:
        raise CheckoutError("El token de pre-registro ha expirado. Regístrese nuevamente.")
    except jwt.PyJWTError:
        raise CheckoutError("Token de pre-registro inválido.")


def _generate_user_name(nombre_tienda: str, db: Session) -> str:
    import re
    import unicodedata
    name = unicodedata.normalize("NFKD", nombre_tienda)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    name = re.sub(r"\s+", "_", name.strip().lower())
    name = name[:50]
    base_name = name
    counter = 1
    while db.query(Vendedor).filter(Vendedor.user_name == name).first():
        suffix = f"_{counter}"
        name = f"{base_name[:50 - len(suffix)]}{suffix}"
        counter += 1
    return name


def _run_simulation(vendedor: Vendedor, db: Session) -> None:
    today = date.today()
    start_date = today - timedelta(days=29)

    payload = {
        "datos_basicos": {
            "user_name": vendedor.user_name,
            "nombre_tienda": vendedor.nombre_tienda,
            "codigo_pais": vendedor.codigo_pais or "MX",
            "moneda_local": vendedor.moneda_local or "MXN",
            "tipo_plan": str(vendedor.tipo_plan or 2),
            "email": vendedor.email,
        },
        "metrica_negocio": {
            "ventas_totales_periodo": 50,
            "fecha_inicio_periodo": start_date.isoformat(),
            "fecha_final_periodo": today.isoformat(),
            "ventas_brutas_moneda_local": 15000.00,
            "ventas_brutas_usd": 750.00,
            "unidades_vendidas": 80,
            "visitas_totales": 2500,
            "intencion_compra": 200,
            "ventas_concretadas": 60,
            "precio_promedio_unidad": 187.50,
            "precio_promedio_venta": 250.00,
        },
        "metrica_costo": {
            "ventas_cobradas_total": 14250.00,
            "neto_recibido": 12000.00,
            "cargos_por_venta": 1500.00,
            "costos_envio": 750.00,
            "inversion_ads": 500.00,
            "otros_cargos": 100.00,
            "cargos_envio_full": 200.00,
            "descuento_reputacion": 0.00,
        },
        "metrica_reputacion": {
            "total_reclamos": 2,
            "total_mediaciones": 0,
            "total_canceladas": 1,
            "total_envios_incorrectos": 0,
            "nivel_reputacion": "green",
            "insignia": None,
        },
        "metrica_stock_full": {
            "espacios_p_asignados": 10,
            "espacios_g_asignados": 5,
            "puntaje_calidad": 95,
            "productos_no_aptos_venta": 1,
            "productos_sin_rotacion": 2,
            "productos_antiguedad": 0,
            "productos_exceso_proyeccion": 0,
        },
        "metrica_mi_pagina": {
            "tiene_banner": False,
            "tiene_logo": False,
            "tiene_carruseles": False,
            "categorias_organizadas": False,
        },
    }

    try:
        payload_json = json.dumps(payload, default=str)
        db.execute(text("CALL sp_simular_30_dias(CAST(:p_datos AS jsonb))"), {"p_datos": payload_json})
        db.commit()
        logger.info("Simulación de 30 días completada para vendedor %s", vendedor.user_name)
    except Exception as e:
        db.rollback()
        logger.error("Error al ejecutar simulación de 30 días para %s: %s", vendedor.user_name, e)


def checkout(db: Session, payload: CheckoutRequest) -> CheckoutResponse:

    data = _decode_pre_token(payload.pre_token)

    plan = db.query(Plan).filter(Plan.id == payload.id_plan).first()
    if not plan:
        raise CheckoutError("El plan especificado no existe.")

    existing = db.query(Vendedor).filter(Vendedor.email == data["email"]).first()
    if existing:
        raise CheckoutError("Este correo ya está registrado.")

    existing_admin = db.query(Admin).filter(Admin.email == data["email"]).first()
    if existing_admin:
        raise CheckoutError("Este correo ya está registrado.")

    if not _validate_luhn(payload.numero_tarjeta):
        raise CheckoutError("El número de tarjeta no es válido.")

    card_type = _detect_card_type(payload.numero_tarjeta)
    expiry_date = _build_expiry_date(payload.mes_caducidad, payload.anio_caducidad)

    user_name = _generate_user_name(data["nombre_tienda"], db)

    vendedor = Vendedor(
        user_name=user_name,
        nombre_tienda=data["nombre_tienda"],
        email=data["email"],
        password=hash_data(data["password"]),
        codigo_pais="MX",
        moneda_local="MXN",
        tipo_plan=payload.id_plan,
    )

    db.add(vendedor)
    db.flush()

    tarjeta = Tarjeta(
        id_vendedor=vendedor.id_vendedor,
        nombre_titular=payload.nombre_titular,
        numero_tarjeta=hash_data(payload.numero_tarjeta),
        fecha_expiracion=expiry_date,
        cvv=hash_data(payload.cvv),
        tipo_tarjeta=card_type,
    )

    db.add(tarjeta)
    db.commit()
    db.refresh(vendedor)

    _run_simulation(vendedor, db)

    return CheckoutResponse(
        success=True,
        message=f"Pago procesado. Plan {plan.nombre_plan} activado. Bienvenido {vendedor.user_name}.",
    )
