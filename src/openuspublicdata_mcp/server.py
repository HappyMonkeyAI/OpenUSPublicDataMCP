from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx
from fastmcp import FastMCP

from openuspublicdata_mcp.sources import list_sources

mcp = FastMCP("OpenUSPublicDataMCP")


def envelope(data: Any, source: dict[str, object]) -> dict[str, object]:
    return {"data": data, "source": source, "retrieved_at": datetime.now(UTC).isoformat()}


@mcp.tool
def health_check() -> dict[str, object]:
    """Return server health and the count of registered public-data sources."""
    return {"status": "ok", "source_count": len(list_sources())}


@mcp.tool
def list_public_data_sources() -> dict[str, object]:
    """List registered US public-data sources with jurisdiction and authentication metadata."""
    return envelope(list_sources(), {"name": "OpenUSPublicDataMCP source registry", "url": "local://sources", "official": False, "jurisdiction": "federal", "auth": "none"})


@mcp.tool
def search_data_gov(query: str, limit: int = 10) -> dict[str, object]:
    """Search Data.gov's official catalogue for datasets matching a query."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    response = httpx.get("https://catalog.data.gov/api/3/action/package_search", params={"q": query, "rows": limit}, timeout=20)
    response.raise_for_status()
    payload = response.json()
    return envelope(payload.get("result", {}), {"name": "Data.gov", "url": "https://catalog.data.gov/api/3/action/package_search", "official": True, "jurisdiction": "federal", "auth": "none"})


def main() -> None:
    mcp.run(show_banner=False, log_level="WARNING")


if __name__ == "__main__":
    main()
