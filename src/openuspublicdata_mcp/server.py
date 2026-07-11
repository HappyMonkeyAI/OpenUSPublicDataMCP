from __future__ import annotations

from datetime import UTC, datetime
import os
from typing import Any

import httpx
from fastmcp import FastMCP

from openuspublicdata_mcp.sources import list_sources
from openuspublicdata_mcp.adapters.portals import query_arcgis, query_socrata, search_ckan, search_socrata

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
    if response.status_code == 404:
        raise RuntimeError("Data.gov legacy CKAN package_search endpoint is unavailable; use the site catalogue until a supported API is identified")
    response.raise_for_status()
    payload = response.json()
    return envelope(payload.get("result", {}), {"name": "Data.gov", "url": "https://catalog.data.gov/api/3/action/package_search", "official": True, "jurisdiction": "federal", "auth": "none"})


@mcp.tool
def get_census_state_population(year: int = 2022) -> dict[str, object]:
    """Return Census ACS 5-year total population by US state for a supported year."""
    if not 2009 <= year <= 2022:
        raise ValueError("year must be between 2009 and 2022")
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    api_key = os.getenv("CENSUS_API_KEY")
    if not api_key:
        raise RuntimeError("CENSUS_API_KEY is required by the current Census API endpoint")
    response = httpx.get(url, params={"get": "NAME,B01001_001E", "for": "state:*", "key": api_key}, timeout=20)
    response.raise_for_status()
    rows = response.json()
    return envelope({"columns": rows[0], "rows": rows[1:]}, {"name": "US Census Bureau ACS 5-year", "url": url, "official": True, "jurisdiction": "federal", "auth": "optional_key"})


@mcp.tool
def list_federal_agencies() -> dict[str, object]:
    """Return federal agencies known to USAspending.gov without requiring an API key."""
    url = "https://api.usaspending.gov/api/v2/references/toptier_agencies/"
    response = httpx.get(url, timeout=20)
    response.raise_for_status()
    return envelope(response.json(), {"name": "USAspending.gov", "url": url, "official": True, "jurisdiction": "federal", "auth": "none"})


@mcp.tool
def search_federal_register(query: str, limit: int = 10) -> dict[str, object]:
    """Search official Federal Register documents by full-text term."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    url = "https://www.federalregister.gov/api/v1/documents.json"
    response = httpx.get(url, params={"conditions[term]": query, "per_page": limit}, timeout=20)
    response.raise_for_status()
    return envelope(response.json(), {"name": "Federal Register", "url": url, "official": True, "jurisdiction": "federal", "auth": "none"})


@mcp.tool
def search_usaspending_awards(query: str, limit: int = 10) -> dict[str, object]:
    """Search federal spending awards by keyword through USAspending.gov."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    payload = {"filters": {"keywords": [query], "award_type_codes": ["A", "B", "C", "D"]}, "fields": ["Award ID", "Award Description", "Award Amount", "Recipient Name"], "limit": limit, "page": 1}
    response = httpx.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return envelope(response.json(), {"name": "USAspending.gov", "url": url, "official": True, "jurisdiction": "federal", "auth": "none"})


@mcp.tool
def search_congress_bills(query: str, limit: int = 10) -> dict[str, object]:
    """Search recent Congress.gov bill records; requires CONGRESS_API_KEY."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 250:
        raise ValueError("limit must be between 1 and 250")
    api_key = os.getenv("CONGRESS_API_KEY")
    if not api_key:
        raise RuntimeError("CONGRESS_API_KEY is required by the Congress.gov API")
    url = "https://api.congress.gov/v3/bill"
    response = httpx.get(url, params={"format": "json", "limit": limit, "api_key": api_key}, timeout=20)
    response.raise_for_status()
    return envelope(response.json(), {"name": "Congress.gov API", "url": url, "official": True, "jurisdiction": "federal", "auth": "optional_key"})


@mcp.tool
def search_socrata_catalog(query: str, limit: int = 10) -> dict[str, object]:
    """Discover state and local datasets hosted on Socrata."""
    return envelope(search_socrata(query, limit), {"name": "Socrata catalog", "url": "https://api.us.socrata.com/api/catalog/v1", "official": False, "jurisdiction": "state_or_local", "auth": "none"})


@mcp.tool
def query_socrata_dataset(domain: str, dataset_id: str, limit: int = 100) -> dict[str, object]:
    """Read rows from a Socrata dataset using its domain and four-character dataset ID."""
    return envelope(query_socrata(domain, dataset_id, limit), {"name": "Socrata dataset", "url": f"https://{domain}/resource/{dataset_id}.json", "official": False, "jurisdiction": "state_or_local", "auth": "none"})


@mcp.tool
def query_arcgis_feature_service(service_url: str, where: str = "1=1", limit: int = 100) -> dict[str, object]:
    """Query an ArcGIS REST feature service layer."""
    return envelope(query_arcgis(service_url, where, limit), {"name": "ArcGIS REST feature service", "url": service_url, "official": False, "jurisdiction": "state_or_local", "auth": "none"})


@mcp.tool
def search_ckan_catalog(base_url: str, query: str, limit: int = 10) -> dict[str, object]:
    """Search a CKAN catalogue hosted by a state, county, city or public institution."""
    return envelope(search_ckan(base_url, query, limit), {"name": "CKAN catalogue", "url": base_url, "official": False, "jurisdiction": "state_or_local", "auth": "none"})


def main() -> None:
    mcp.run(show_banner=False, log_level="WARNING")


if __name__ == "__main__":
    main()
