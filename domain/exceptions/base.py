from typing import Optional, Union


class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[dict] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, entity: str, identifier: Union[int, str]):
        self.entity = entity
        self.identifier = identifier
        super().__init__(
            message=f"{entity} con identificador '{identifier}' no encontrado",
            code="NOT_FOUND",
            status_code=404,
            details={"entity": entity, "identifier": str(identifier)},
        )


class DuplicateException(AppException):
    def __init__(self, entity: str, field: str, value: str):
        self.entity = entity
        self.field = field
        self.value = value
        super().__init__(
            message=f"{entity} con {field} '{value}' ya existe",
            code="DUPLICATE_ENTRY",
            status_code=409,
            details={"entity": entity, "field": field, "value": value},
        )
