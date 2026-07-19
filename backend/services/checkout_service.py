import json
import logging
import random
from datetime import date, timedelta
import jwt
import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.checkout_schema import CheckoutRequest, CheckoutResponse
from models.tarjeta_model import Tarjeta
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from models.plan_model import Plan
from auth.hash_handler import hash_data
from auth.jwt_handler import ALGORITHM, create_access_token
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

    user_name = data.get("usuario_ml", _generate_user_name(data["nombre_tienda"], db))

    existing_user = db.query(Vendedor).filter(Vendedor.user_name == user_name).first()
    if existing_user:
        raise CheckoutError(f"El usuario de Mercado Libre '{user_name}' ya está registrado. Inicia sesión o usa otro nombre de usuario.")

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

    access_token = create_access_token(data={"sub": str(vendedor.id_vendedor), "role": "vendedor"})

    return CheckoutResponse(
        success=True,
        message=f"Pago procesado. Plan {plan.nombre_plan} activado. Bienvenido {vendedor.user_name}.",
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
        role="vendedor",
        id_vendedor=vendedor.id_vendedor,
    )


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


def _fetch_from_mockoon() -> dict:
    mock_id = random.randint(16, 22)
    path = settings.mockoon_endpoint.replace("{id}", str(mock_id))
    url = f"{settings.mockoon_url.rstrip('/')}{path}"
    logger.info("Obteniendo datos desde Mockoon: GET %s", url)
    with httpx.Client(timeout=5) as client:
        resp = client.get(url)
        resp.raise_for_status()
        data = resp.json()
    logger.info("Mockoon respondió OK para vendedor ID %s", mock_id)
    return data


def sync_with_mockoon(db: Session, vendedor: Vendedor, usuario_ml: str | None = None) -> dict:
    try:
        mockoon_data = _fetch_from_mockoon()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        logger.error("Error al conectar con Mockoon: %s", e)
        raise CheckoutError(f"No se pudo conectar con Mockoon: {e}")

    datos_basicos_mock = mockoon_data.get("datos_basicos", {})

    if usuario_ml:
        vendedor.user_name = usuario_ml
    vendedor.codigo_pais = datos_basicos_mock.get("codigo_pais", vendedor.codigo_pais)
    vendedor.moneda_local = datos_basicos_mock.get("moneda_local", vendedor.moneda_local)
    if datos_basicos_mock.get("acces_token"):
        vendedor.access_token = datos_basicos_mock["acces_token"]
    if datos_basicos_mock.get("refresh_token"):
        vendedor.refresh_token = datos_basicos_mock["refresh_token"]

    db.commit()
    db.refresh(vendedor)

    today = date.today()
    start_date = today - timedelta(days=29)

    plan_map = {"Clasico": "1", "Premium": "2", "Básico": "1"}
    raw_plan = str(datos_basicos_mock.get("tipo_plan", ""))
    tipo_plan_str = plan_map.get(raw_plan, str(vendedor.tipo_plan or 2))

    payload = {
        "datos_basicos": {
            "user_name": vendedor.user_name,
            "nombre_tienda": vendedor.nombre_tienda,
            "codigo_pais": vendedor.codigo_pais or "MX",
            "moneda_local": vendedor.moneda_local or "MXN",
            "tipo_plan": tipo_plan_str,
            "email": vendedor.email,
        },
        "metrica_negocio": mockoon_data.get("metricas_negocio", mockoon_data.get("metrica_negocio", {})),
        "metrica_costo": mockoon_data.get("metricas_costo", mockoon_data.get("metrica_costo", {})),
        "metrica_reputacion": mockoon_data.get("metricas_reputacion", mockoon_data.get("metrica_reputacion", {})),
        "metrica_stock_full": mockoon_data.get("metricas_stock_full", mockoon_data.get("metrica_stock_full", {})),
        "metrica_mi_pagina": mockoon_data.get("metricas_mi_pagina", mockoon_data.get("metrica_mi_pagina", {})),
    }

    payload["datos_basicos"]["tipo_plan"] = tipo_plan_str
    payload["metrica_negocio"]["fecha_inicio_periodo"] = start_date.isoformat()
    payload["metrica_negocio"]["fecha_final_periodo"] = today.isoformat()

    try:
        payload_json = json.dumps(payload, default=str)
        db.execute(text("CALL sp_simular_30_dias(CAST(:p_datos AS jsonb))"), {"p_datos": payload_json})
        db.commit()
        logger.info("Simulación de 30 días completada para vendedor %s", vendedor.user_name)
    except Exception as e:
        db.rollback()
        logger.error("Error al ejecutar simulación de 30 días para %s: %s", vendedor.user_name, e)
        raise CheckoutError(f"Error en la simulación de datos: {e}")

    return {"status": "success", "message": "Datos sincronizados con Mockoon y simulación de 30 días completada."}
