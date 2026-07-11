# OpenUSPublicDataMCP

Federal-first, no-key-first MCP access to high-value US public data sources.

This is the US counterpart to `OpenUKPublicDataMCP`, but it deliberately separates federal coverage from the fragmented state and local ecosystem. Reusable Socrata, ArcGIS REST and CKAN adapters will come after the federal contract is stable.

## Current bootstrap status

- FastMCP server with stdio transport
- source registry with provenance metadata
- `health_check`
- `list_public_data_sources`
- `search_data_gov` against the official Data.gov CKAN API (endpoint under re-discovery after live 404)
- `get_census_state_population` against the official Census ACS API (optional key)
- `list_federal_agencies` against the official USAspending API (no key)
- `search_federal_register` against the official Federal Register API (no key)
- `search_usaspending_awards` against the official USAspending awards API (no key)
- `search_congress_bills` against the official Congress.gov API (optional key)
- `search_socrata_catalog` and `query_socrata_dataset`
- `query_arcgis_feature_service`
- `search_ckan_catalog`
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

1. Federal catalogue and geography foundations.
2. Census state population, Congress.gov, Federal Register and USAspending adapters.
3. Generic state/local portal adapters: Socrata, ArcGIS REST and CKAN.
4. Curated state packs and local discovery.

See `docs/plans/2026-07-11-openuspublicdata-mcp-bootstrap.md` and `research/LINKS.md`.
