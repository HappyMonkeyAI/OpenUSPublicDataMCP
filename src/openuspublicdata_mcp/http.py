from __future__ import annotations

import time
from typing import Any

import httpx


import atexit


RETRYABLE_STATUS = {429, 500, 502, 503, 504}


# Share a persistent connection-reusing client
client = httpx.Client(timeout=20.0)


@atexit.register
def close_client() -> None:
    """Close the persistent HTTP client."""
    client.close()


def request_json(method: str, url: str, *, params: dict[str, Any] | None = None, json: Any = None, timeout: float = 20, retries: int = 2) -> Any:
    """Fetch JSON with bounded retries for rate limits and transient upstream failures."""
    for attempt in range(retries + 1):
        try:
            response = client.request(method, url, params=params, json=json, timeout=timeout)
            if response.status_code not in RETRYABLE_STATUS or attempt == retries:
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as exc:
            is_non_retryable_status = (
                isinstance(exc, httpx.HTTPStatusError)
                and exc.response.status_code not in RETRYABLE_STATUS
            )
            if is_non_retryable_status or attempt == retries:
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

        if attempt < retries:
            time.sleep(0.2 * (attempt + 1))

