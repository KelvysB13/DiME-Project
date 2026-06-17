from typing import Optional
from domain.exceptions.base import AppException


class DatabaseException(AppException):
    def __init__(self, message: str, original_error: Optional[str] = None):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details={"original_error": original_error} if original_error else {},
        )
