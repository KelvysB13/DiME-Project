from datetime import date
import jwt
from sqlalchemy.orm import Session
from schemas.checkout_schema import CheckoutRequest, CheckoutResponse
from models.tarjeta_model import Tarjeta
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from models.plan_model import Plan
from auth.hash_handler import hash_data
from auth.jwt_handler import ALGORITHM
from core.config import settings


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

    return CheckoutResponse(
        success=True,
        message=f"Pago procesado. Plan {plan.nombre_plan} activado. Bienvenido {vendedor.user_name}.",
    )
