from datetime import date
from sqlalchemy.orm import Session
from schemas.payment_method_schema import PaymentMethodRequest, PaymentMethodResponse
from models.tarjeta_model import Tarjeta
from auth.hash_handler import hash_data


class PaymentMethodError(Exception):
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

    raise PaymentMethodError("Tipo de tarjeta no soportado. Solo se aceptan Visa y MasterCard.")


def _build_expiry_date(month: int, year: int) -> date:

    year_full = 2000 + year
    expiry = date(year_full, month, 1)

    today = date.today()
    if expiry.replace(day=1) <= date(today.year, today.month, 1):
        raise PaymentMethodError("La tarjeta está vencida.")

    return expiry


def update_payment_method(db: Session, payload: PaymentMethodRequest, vendedor_id: int) -> PaymentMethodResponse:

    if not _validate_luhn(payload.numero_tarjeta):
        raise PaymentMethodError("El número de tarjeta no es válido.")

    tipo = _detect_card_type(payload.numero_tarjeta)
    fecha_expiracion = _build_expiry_date(payload.mes_caducidad, payload.anio_caducidad)

    tarjeta = db.query(Tarjeta).filter(Tarjeta.id_vendedor == vendedor_id).first()

    if tarjeta:
        tarjeta.nombre_titular = payload.nombre_titular
        tarjeta.numero_tarjeta = hash_data(payload.numero_tarjeta)
        tarjeta.fecha_expiracion = fecha_expiracion
        tarjeta.cvv = hash_data(payload.cvv)
        tarjeta.tipo_tarjeta = tipo
        msg = "Método de pago actualizado exitosamente."
    else:
        tarjeta = Tarjeta(
            id_vendedor=vendedor_id,
            nombre_titular=payload.nombre_titular,
            numero_tarjeta=hash_data(payload.numero_tarjeta),
            fecha_expiracion=fecha_expiracion,
            cvv=hash_data(payload.cvv),
            tipo_tarjeta=tipo,
        )
        db.add(tarjeta)
        msg = "Método de pago registrado exitosamente."

    db.commit()
    db.refresh(tarjeta)

    return PaymentMethodResponse(success=True, message=msg)
