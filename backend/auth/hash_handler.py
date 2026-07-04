import hashlib
import bcrypt

def pre_hash_data(data: str) -> bytes:
    return hashlib.sha256(data.encode("utf-8")).hexdigest().encode("utf-8")

def hash_data(data: str) -> str:

    if not data:
        raise ValueError("El dato no puede estar vacío.")
    
    return bcrypt.hashpw(pre_hash_data(data), bcrypt.gensalt()).decode("utf-8")

def verify_hash(plain_data: str, hashed_data: str) -> bool:

    try:
        return bcrypt.checkpw(pre_hash_data(plain_data), hashed_data.encode("utf-8"))
    
    except Exception:
        return False
