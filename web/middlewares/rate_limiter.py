import math
import time
from typing import Dict, List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

_FORWARDED_FOR_HEADER = "x-forwarded-for"


class RateLimit:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window


DEFAULT_RATE_LIMIT = RateLimit(requests=100, window=60)

ENDPOINT_LIMITS: Dict[str, RateLimit] = {
    "/auth/login": RateLimit(requests=5, window=60),
    "/auth/register": RateLimit(requests=3, window=3600),
}


def get_limit_for_path(path: str) -> RateLimit:
    return ENDPOINT_LIMITS.get(path, DEFAULT_RATE_LIMIT)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._store: Dict[str, List[float]] = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = self._extract_ip(request)
        path = request.url.path
        limit = get_limit_for_path(path)
        store_key = f"{client_ip}:{path}"

        now = time.time()
        window_start = now - limit.window

        if store_key not in self._store:
            self._store[store_key] = []

        timestamps = [t for t in self._store[store_key] if t > window_start]
        self._store[store_key] = timestamps

        if len(timestamps) >= limit.requests:
            retry_after = math.ceil(timestamps[0] + limit.window - now) if timestamps else limit.window
            response = JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Límite de {limit.requests} peticiones en {limit.window}s excedido",
                    "retry_after_seconds": retry_after,
                },
            )
            response.headers["X-RateLimit-Limit"] = str(limit.requests)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["Retry-After"] = str(retry_after)
            return response

        self._store[store_key].append(now)
        remaining = limit.requests - len(self._store[store_key])

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit.requests)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        return response

    def _extract_ip(self, request: Request) -> str:
        forwarded = request.headers.get(_FORWARDED_FOR_HEADER)
        if forwarded:
            return forwarded.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"
