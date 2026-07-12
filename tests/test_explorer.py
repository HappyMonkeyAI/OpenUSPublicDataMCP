from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from openuspublicdata_mcp.http_server import app


@pytest.mark.asyncio
async def test_explorer_catalogue_preserves_jurisdiction_and_coverage_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/explorer/catalogue")

    assert response.status_code == 200
    body = response.json()
    assert body["state_count"] == 51
    assert body["curated_state_count"] == 5
    layers = {layer["id"]: layer for layer in body["layers"]}
    assert layers["states"]["default_enabled"] is True
    assert layers["curated-portals"]["coverage_status"] == "selected_states"
    assert layers["federal-sources"]["jurisdiction"] == "federal"


@pytest.mark.asyncio
async def test_state_entities_use_normalized_map_contract():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/explorer/states")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 51
    california = next(entity for entity in body["entities"] if entity["id"] == "CA")
    assert california["type"] == "state"
    assert california["properties"]["fips"] == "06"
    assert california["properties"]["curated_portal"]["platform"] == "ckan"
    assert isinstance(california["latitude"], float)
    assert isinstance(california["longitude"], float)
    assert set(california) == {
        "id", "type", "title", "latitude", "longitude", "observed_at", "severity", "properties"
    }


@pytest.mark.asyncio
async def test_source_discovery_filters_without_calling_upstream_services():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/explorer/sources", params={"q": "federal"})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "federal"
    assert body["count"] >= 5
    assert all(source["jurisdiction"] == "federal" for source in body["sources"])
    assert all("auth" in source and "licence" in source for source in body["sources"])


@pytest.mark.asyncio
async def test_state_detail_reports_missing_curated_portal_honestly():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/explorer/states/MA")

    assert response.status_code == 200
    body = response.json()
    assert body["state_code"] == "MA"
    assert body["curated_portal"] is None
    assert body["coverage_status"] == "registry_only"
