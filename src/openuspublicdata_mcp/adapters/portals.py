from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import httpx


def _check_limit(limit: int) -> None:
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")


def search_socrata(query: str, limit: int = 10) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("query must not be empty")
    _check_limit(limit)
    url = "https://api.us.socrata.com/api/catalog/v1"
    response = httpx.get(url, params={"q": query, "limit": limit}, timeout=20)
    response.raise_for_status()
    return response.json()


def query_socrata(domain: str, dataset_id: str, limit: int = 100) -> list[dict[str, Any]]:
    _check_limit(limit)
    if not domain or "." not in domain or not dataset_id.strip():
        raise ValueError("domain and dataset_id are required")
    url = f"https://{domain}/resource/{dataset_id}.json"
    response = httpx.get(url, params={"$limit": limit}, timeout=20)
    response.raise_for_status()
    return response.json()


def query_arcgis(service_url: str, where: str = "1=1", limit: int = 100) -> dict[str, Any]:
    _check_limit(limit)
    parsed = urlparse(service_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("service_url must be an absolute HTTP(S) URL")
    response = httpx.get(f"{service_url.rstrip('/')}/query", params={"where": where, "outFields": "*", "f": "json", "resultRecordCount": limit}, timeout=30)
    response.raise_for_status()
    return response.json()


def search_ckan(base_url: str, query: str, limit: int = 10) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("query must not be empty")
    _check_limit(limit)
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("base_url must be an absolute HTTP(S) URL")
    url = f"{base_url.rstrip('/')}/api/3/action/package_search"
    response = httpx.get(url, params={"q": query, "rows": limit}, timeout=20)
    response.raise_for_status()
    return response.json()
