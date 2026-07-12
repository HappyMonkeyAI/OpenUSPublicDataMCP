from __future__ import annotations

import time
from typing import Any

import httpx


RETRYABLE_STATUS = {429, 500, 502, 503, 504}


# Share a persistent connection-reusing client
client = httpx.Client(timeout=20.0)


def request_json(method: str, url: str, *, params: dict[str, Any] | None = None, json: Any = None, timeout: float = 20, retries: int = 2) -> Any:
    """Fetch JSON with bounded retries for rate limits and transient upstream failures."""
    last_response: httpx.Response | None = None
    for attempt in range(retries + 1):
        try:
            response = client.request(method, url, params=params, json=json, timeout=timeout)
            last_response = response
            if response.status_code not in RETRYABLE_STATUS or attempt == retries:
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as exc:
            # Catch HTTP status, connection, and timeout errors to redact sensitive parameters (like keys/tokens)
            if params and any(k in params for k in ("key", "api_key")):
                sanitized_params = {
                    k: ("REDACTED" if k in ("key", "api_key") else v)
                    for k, v in params.items()
                }
                err_msg = f"HTTP request to {url} failed: {exc.__class__.__name__}"
                if isinstance(exc, httpx.HTTPStatusError):
                    err_msg += f" status_code={exc.response.status_code}"
                raise RuntimeError(f"{err_msg} with params {sanitized_params}") from None
            raise
        time.sleep(0.2 * (attempt + 1))
    
    if params and any(k in params for k in ("key", "api_key")):
        sanitized_params = {
            k: ("REDACTED" if k in ("key", "api_key") else v)
            for k, v in params.items()
        }
        raise RuntimeError(f"Request to {url} failed with params {sanitized_params}")
    raise RuntimeError(f"Request to {url} failed")
