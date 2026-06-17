import time
import uuid
import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from domain.exceptions import NotFoundException, DuplicateException, BusinessException, AppException

logger = logging.getLogger("api")


def register_middleware(app: FastAPI):
    """Register all middleware and exception handlers on the FastAPI app."""

    # ── Security headers middleware ──
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # ── Correlation ID middleware ──
    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response

    # ── Request logging and timing middleware ──
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "%.3fms %s %s -> %s [%s]",
            duration_ms,
            request.method,
            request.url.path,
            response.status_code,
            getattr(request.state, "correlation_id", "-"),
        )
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.1f}"
        return response

    # ── Exception handlers ──

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "NOT_FOUND",
                    "message": str(exc),
                    "details": {"entity": exc.entity, "identifier": exc.identifier},
                }
            },
        )

    @app.exception_handler(DuplicateException)
    async def duplicate_handler(request: Request, exc: DuplicateException):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "DUPLICATE_ENTRY",
                    "message": str(exc),
                    "details": {"entity": exc.entity, "field": exc.field, "value": exc.value},
                }
            },
        )

    @app.exception_handler(BusinessException)
    async def business_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": exc.code or "BUSINESS_ERROR",
                    "message": str(exc),
                    "details": {},
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Error interno del servidor",
                    "details": {},
                }
            },
        )
