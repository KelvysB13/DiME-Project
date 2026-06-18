import os
import time
import logging
import requests
from infrastructure.external.adapters.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)


class BackendAdapter:
    def __init__(self, base_url: str, timeout: int = 10, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.circuit_breaker = CircuitBreaker()
        self.use_mock = os.getenv("USE_BACKEND_MOCK", "false").lower() == "true"

    def _build_url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _do_request(self, method: str, path: str, **kwargs) -> dict:
        url = self._build_url(path)
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method, url, timeout=self.timeout, **kwargs
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logger.warning(
                    "Request failed (attempt %d/%d): %s %s - %s",
                    attempt + 1, self.max_retries, method, url, e,
                )
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise

    def request(self, method: str, path: str, **kwargs) -> dict:
        if self.use_mock:
            return self._mock_request(method, path)
        return self.circuit_breaker.call(self._do_request, method, path, **kwargs)

    def _mock_request(self, method: str, path: str) -> dict:
        return {"status": "ok", "mock": True, "method": method, "path": path}
