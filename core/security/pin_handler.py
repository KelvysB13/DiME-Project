import secrets
import hashlib


def generate_validation_pin(length: int = 6) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(length))


def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()


def verify_pin(pin: str, pin_hash: str) -> bool:
    return hashlib.sha256(pin.encode()).hexdigest() == pin_hash
