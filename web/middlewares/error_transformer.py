from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions import NotFoundException, DuplicateException, BusinessException


def error_response(message: str, error_code: str = "BAD_REQUEST", status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
            "code": error_code,
        }
    )


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": str(exc),
                "code": "NOT_FOUND",
                "entity": exc.entity,
                "identifier": exc.identifier,
            },
        )

    @app.exception_handler(DuplicateException)
    async def duplicate_handler(request: Request, exc: DuplicateException):
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": str(exc),
                "code": "DUPLICATE_ENTRY",
                "entity": exc.entity,
                "field": exc.field,
                "value": exc.value,
            },
        )

    @app.exception_handler(BusinessException)
    async def business_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": str(exc),
                "code": exc.code or "BUSINESS_ERROR",
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        import logging
        logger = logging.getLogger("api")
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error interno del servidor",
                "code": "INTERNAL_ERROR",
            },
        )
