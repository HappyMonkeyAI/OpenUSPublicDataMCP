from __future__ import annotations

import time
from typing import Any

import httpx


RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def request_json(method: str, url: str, *, params: dict[str, Any] | None = None, json: Any = None, timeout: float = 20, retries: int = 2) -> Any:
    """Fetch JSON with bounded retries for rate limits and transient upstream failures."""
    last_response: httpx.Response | None = None
    for attempt in range(retries + 1):
        response = httpx.request(method, url, params=params, json=json, timeout=timeout)
        last_response = response
        if response.status_code not in RETRYABLE_STATUS or attempt == retries:
            response.raise_for_status()
            return response.json()
        time.sleep(0.2 * (attempt + 1))
    raise RuntimeError(f"request failed without response: {url}") if last_response is None else RuntimeError(f"request failed: {url}")
