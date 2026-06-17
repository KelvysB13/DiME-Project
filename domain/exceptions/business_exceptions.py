from typing import Optional
from domain.exceptions.base import AppException


class BusinessException(AppException):
    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(
            message=message,
            code=code or "BUSINESS_ERROR",
            status_code=400,
        )


class ValidationException(AppException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details or {},
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "No tienes permisos para acceder a este recurso"):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Autenticación requerida"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )


class RateLimitException(AppException):
    def __init__(self, message: str = "Demasiadas solicitudes. Intente más tarde"):
        super().__init__(
            message=message,
            code="RATE_LIMITED",
            status_code=429,
        )
