import hashlib
import bcrypt

# Función para pre-hash de la contraseña antes de aplicar bcrypt.
def pre_hash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")

# Función para hashear la contraseña utilizando bcrypt.
def hash_password(password: str) -> str:

    if not password:
        raise ValueError("La contraseña no puede estar vacía.")

    return bcrypt.hashpw(pre_hash_password(password), bcrypt.gensalt()).decode("utf-8")

# Función para verificar la contraseña ingresada contra el hash almacenado.
def verify_password(plain_password: str, hashed_password: str) -> bool:

    try:
        return bcrypt.checkpw(pre_hash_password(plain_password), hashed_password.encode("utf-8"))

    except Exception:
        return False
