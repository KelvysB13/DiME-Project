from functools import wraps
from typing import Callable
from fastapi import HTTPException, Request, status
from config.settings import ALLOWED_ROLES
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RoleGuard:
    def __init__(self, allowed_roles: list[str] | None = None):
        self.allowed_roles = allowed_roles or list(ALLOWED_ROLES)
        logger.info(f"RoleGuard initialized with roles: {self.allowed_roles}")

    def is_valid_role(self, role: str) -> bool:
        return role in self.allowed_roles

    def validate_role(self, user_role: str, required_roles: list[str]) -> bool:
        if not user_role:
            raise ValueError("User role cannot be empty")
        if not isinstance(required_roles, list) or len(required_roles) == 0:
            raise ValueError("Required roles list cannot be empty")
        has_permission = user_role in required_roles
        if has_permission:
            logger.info(f"Access granted for role: {user_role}")
        else:
            logger.warning(f"Access denied. Role '{user_role}' not in {required_roles}")
        return has_permission

    def require_role(self, required_roles: list[str]) -> Callable:
        if not required_roles:
            raise ValueError("At least one role must be specified")

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                request = None
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                if not request:
                    request = kwargs.get("request")
                if not request:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Request object not found"
                    )

                user_data = getattr(request.state, "user", None)
                user_role = user_data.get("role") if user_data else None

                if not user_role:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permisos para realizar esta accion"
                    )

                if user_role not in required_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permisos para realizar esta accion"
                    )

                return await func(*args, **kwargs)
            return wrapper
        return decorator


role_guard = RoleGuard()
require_role = role_guard.require_role
