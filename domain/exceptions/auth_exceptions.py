from domain.exceptions.base import AppException


class InvalidCredentialsException(AppException):
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(
            message=message,
            code="INVALID_CREDENTIALS",
            status_code=401,
        )


class TokenExpiredException(AppException):
    def __init__(self, message: str = "El token ha expirado"):
        super().__init__(
            message=message,
            code="TOKEN_EXPIRED",
            status_code=401,
        )


class InvalidTokenException(AppException):
    def __init__(self, message: str = "Token inválido o manipulado"):
        super().__init__(
            message=message,
            code="INVALID_TOKEN",
            status_code=401,
        )
