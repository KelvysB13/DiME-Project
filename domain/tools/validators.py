import re
from typing import Annotated
from pydantic import AfterValidator


def validar_telefono_venezuela(v: str) -> str:
    telefono = re.sub(r"[\s\-\(\)]", "", v)
    if telefono.startswith("0"):
        telefono = "+58" + telefono[1:]
    elif telefono.startswith("58") and not telefono.startswith("+"):
        telefono = "+" + telefono
    elif not telefono.startswith("+58"):
        telefono = "+58" + telefono
    patron = r"^\+58\d{10}$"
    if not re.match(patron, telefono):
        raise ValueError("Formato de teléfono inválido. Debe ser +58 seguido de 10 dígitos.")
    return telefono


TelefonoVenezuela = Annotated[str, AfterValidator(validar_telefono_venezuela)]
