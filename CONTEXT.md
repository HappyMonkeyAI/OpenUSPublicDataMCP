# CONTEXT — OpenUSPublicDataMCP

## Mission

Build an agent-grade MCP gateway for high-value US public data. Start with federal sources, then expand through reusable state/local portal adapters without pretending that every jurisdiction is uniform.

## Stack

- Python 3.11+
- FastMCP
- httpx
- pytest, pytest-asyncio, respx
- `src/` package layout

## Non-negotiables

1. Federal-first and no-key-first where practical.
2. Official sources preferred; community sources clearly labelled.
3. Every external result includes source, jurisdiction, auth mode and retrieval time.
4. No scraping in the core when an API or bulk download exists.
5. Optional credentials never prevent server startup.
6. Read-only tools in the initial project.
7. Do not claim “all US government data”.

## Response contract

```json
{
  "data": {},
  "source": {"name": "", "url": "", "official": true, "jurisdiction": "federal", "auth": "none"},
  "retrieved_at": "..."
}
```

## Completed Q2 foundation

- Federal tools: USAspending, Federal Register, Census and Congress.gov optional-key paths.
- Generic Socrata, ArcGIS REST/Hub and CKAN adapters.
- Curated state packs: CA, NY, TX, WA and FL.
- Shared retrying HTTP helper, typed source metadata and state/FIPS resolution.
- Stdio plus Streamable HTTP transport; HTTP MCP session verified with the MCP SDK.
- DynamicMCPProxy catalogue artefact and Hermes setup documentation.
- Q2 report: `docs/tests/Q2-executive-report.md`.

## Next build slice

Climate/environment vertical workflow across federal and state sources: NOAA/EPA adapters, curated environmental datasets, freshness/licence metadata, comparison tools, and county/Census geography.

## Planned source layers

- Federal: Data.gov, Census, Congress.gov, Federal Register, USAspending, BLS, BEA, NOAA, EPA, FDA, CDC and USDA.
- State/local platform adapters: Socrata, ArcGIS REST, CKAN and curated custom sources.
- Geography: Census geographies and national boundary datasets.

## What not to do

- Do not write 50 bespoke state servers before proving generic portal adapters.
- Do not silently mix federal, state and local figures with incompatible definitions.
- Do not hide API-key requirements or licensing uncertainty.
- Do not return uncited raw upstream payloads as authoritative answers.
