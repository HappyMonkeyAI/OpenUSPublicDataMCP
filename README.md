# OpenUSPublicDataMCP

Federal-first, no-key-first MCP access to high-value US public data sources.

This is the US counterpart to `OpenUKPublicDataMCP`, but it deliberately separates federal coverage from the fragmented state and local ecosystem. Reusable Socrata, ArcGIS REST and CKAN adapters provide platform coverage without pretending that jurisdictions share one schema.

## Current bootstrap status

- FastMCP server with stdio transport
- source registry with provenance metadata
- `health_check`
- `list_public_data_sources`
- `find_us_data_sources` — filter the registry by jurisdiction or platform
- `resolve_us_geography` — resolve state names/abbreviations/city-state strings to state FIPS
- `search_data_gov` against the official Data.gov CKAN API (endpoint under re-discovery after live 404)
- `get_census_state_population` against the official Census ACS API (optional key)
- `list_federal_agencies` against the official USAspending API (no key)
- `search_federal_register` against the official Federal Register API (no key)
- `search_usaspending_awards` against the official USAspending awards API (no key)
- `search_congress_bills` against the official Congress.gov API (optional key)
- `search_socrata_catalog` and `query_socrata_dataset`
- `query_arcgis_feature_service`
- `search_ckan_catalog`
- `list_curated_state_portals` — California, New York, Texas, Washington and Florida
- `search_state_data` — dispatch to the selected state's curated portal
- mocked tests and project verification spine

## Quick start

```bash
cd /home/stephen/projects/OpenUSPublicDataMCP
python3.11 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest
fastmcp inspect src/openuspublicdata_mcp/server.py:mcp
fastmcp list src/openuspublicdata_mcp/server.py --json
fastmcp call src/openuspublicdata_mcp/server.py search_data_gov query='climate' limit=3 --json
```

## Direction

1. Curated state packs and local discovery.
2. Federal breadth: BLS, BEA, NOAA, EPA, FDA, CDC and USDA.
3. County FIPS, congressional districts and richer Census geography.
4. HTTP deployment, DynamicMCPProxy and Hermes registration.

See `docs/plans/2026-07-11-openuspublicdata-mcp-bootstrap.md` and `research/LINKS.md`.

## HTTP transport

```bash
OPENUS_PORT=8787 .venv/bin/openuspublicdata-http
curl http://127.0.0.1:8787/health
# MCP endpoint: http://127.0.0.1:8787/mcp
```

The DynamicMCPProxy catalogue entry is in `integrations/dynamic-mcp-proxy-user-catalogue-entry.json`. Hermes can use the stdio server directly:

```bash
hermes config set mcp_servers.openuspublicdata.command "/home/stephen/projects/OpenUSPublicDataMCP/.venv/bin/python"
hermes config set mcp_servers.openuspublicdata.args '["-m", "openuspublicdata_mcp.server"]'
```
