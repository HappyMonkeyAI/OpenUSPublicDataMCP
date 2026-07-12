# US Public Data — Q2 2026 Executive Snapshot (Test Brief)

**Prepared:** 11 July 2026  
**Method:** OpenUSPublicDataMCP live tool calls, official upstream API verification, mocked adapter tests, FastMCP inspection and a real Streamable HTTP MCP session.  
**Scope note:** This is an engineering validation brief for the US public-data MCP gateway. It is not an official US statistical publication and does not claim complete federal, state or local coverage.

---

## Headline

OpenUSPublicDataMCP has moved from a federal bootstrap to a working, multi-jurisdiction MCP gateway. The Q2 build now exposes **16 tools**, covers **8 registered source records**, supports federal and optional-key sources, dispatches searches across **five curated state portals**, and is verified over both stdio and Streamable HTTP. The principal design finding is confirmed: federal APIs are comparatively tractable, while state coverage is best handled through jurisdiction-aware platform adapters rather than one imagined national API.

---

## 1. Q2 delivery summary

| Capability | Result |
|---|---|
| Federal-first server | Implemented |
| Source-cited envelopes | Implemented |
| No-key federal tools | Implemented where upstream permits |
| Optional Census/Congress keys | Documented and startup-safe |
| Socrata adapter | Implemented |
| ArcGIS REST/Hub adapter | Implemented |
| CKAN adapter | Implemented |
| State/FIPS resolution | Implemented for states and abbreviations |
| Curated state packs | California, New York, Texas, Washington, Florida |
| HTTP transport | Implemented and MCP SDK verified |
| DynamicMCPProxy catalogue entry | Added |
| Hermes configuration instructions | Added |

---

## 2. Federal coverage

The server currently includes these federal-facing tools:

- `list_federal_agencies` — USAspending agency reference data.
- `search_federal_register` — Federal Register document search.
- `search_usaspending_awards` — USAspending award search.
- `get_census_state_population` — Census ACS state population data; requires `CENSUS_API_KEY` in the current upstream environment.
- `search_congress_bills` — Congress.gov bill search; requires `CONGRESS_API_KEY`.
- `search_data_gov` — retained with explicit legacy-endpoint warning after the old CKAN action route returned HTTP 404.

### Live federal checks

| Check | Result |
|---|---|
| Federal Register search for `climate` | HTTP success; 10,000 matching documents reported |
| Federal Register sample | `Rescission of Climate-Related Disclosure Rules` |
| USAspending award search | 2 results in the verified contract-award slice |
| USAspending sample award | `WCO00200209D68D02101` |
| Census/Congress credential behaviour | Missing credentials fail clearly without breaking server startup |

**Primary sources:** [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1), [USAspending API](https://api.usaspending.gov/), [Census API](https://www.census.gov/data/developers/data-sets.html), [Congress.gov API](https://api.congress.gov/).

---

## 3. State and local platform coverage

The platform layer deliberately preserves upstream differences while adding a common MCP shape.

| State pack | Official portal | Platform | Live result |
|---|---|---|---|
| California | [data.ca.gov](https://data.ca.gov) | CKAN | Search responded successfully; climate query returned 0 results in the smoke run |
| New York | [data.ny.gov](https://data.ny.gov) | Socrata | Climate query returned 2 results |
| Texas | [data.texas.gov](https://data.texas.gov) | Socrata | Search responded successfully; climate query returned 0 results in the smoke run |
| Washington | [data.wa.gov](https://data.wa.gov) | Socrata | Climate query returned 2 results |
| Florida | [Florida Geospatial Open Data Portal](https://geodata.floridagio.gov/) | ArcGIS Hub | Climate search returned 10,000 results, capped by upstream response behaviour |

The state tools are:

- `list_curated_state_portals`
- `search_state_data`

A zero-result search is treated as a valid upstream response, not as evidence that a state has no relevant data. Dataset ranking, freshness and subject-specific curation remain next-phase work.

---

## 4. Geography and provenance

`resolve_us_geography` currently resolves state names, abbreviations and city/state strings to state metadata.

Example:

```text
Austin, Texas
→ Texas / TX / state FIPS 48
```

Every tool response carries a provenance envelope containing the returned data, source metadata and retrieval timestamp. Source records include jurisdiction, platform, official status and authentication mode.

**Current limitation:** county FIPS, congressional districts, Census tracts and block groups are not yet implemented.

---

## 5. HTTP and MCP integration

The server supports both local stdio and Streamable HTTP operation.

```text
Health: http://127.0.0.1:8787/health
MCP:    http://127.0.0.1:8787/mcp
```

### Live HTTP verification

- `/health` returned HTTP 200:

```json
{"status":"ok","source_count":8}
```

- MCP SDK `initialize` succeeded.
- MCP SDK `list_tools` returned all **16 tools**.
- `search_state_data` was confirmed discoverable over HTTP.

The DynamicMCPProxy catalogue artefact is:

```text
integrations/dynamic-mcp-proxy-user-catalogue-entry.json
```

The server can also be registered directly with Hermes using the documented stdio configuration.

---

## 6. Verification verdict

| Check | Result |
|---|---|
| Unit and mocked adapter tests | **20 passed** |
| Python compilation | Passed |
| FastMCP inspection | **16 tools** |
| Federal live smoke checks | Passed |
| Socrata live smoke checks | Passed |
| CKAN live smoke checks | Passed |
| ArcGIS live smoke checks | Passed |
| State-pack live smoke checks | Passed for all 5 curated states |
| HTTP health endpoint | HTTP 200 |
| Streamable HTTP MCP initialize/list-tools | Passed |
| Git diff check | Passed |

Verification commands:

```bash
cd OpenUSPublicDataMCP
.venv/bin/pytest -q
.venv/bin/python -m compileall -q src tests
.venv/bin/fastmcp inspect src/openuspublicdata_mcp/server.py:mcp
OPENUS_PORT=8787 .venv/bin/openuspublicdata-http
```

---

## 7. Risks and limitations

1. **No uniform US catalogue:** state and local portals remain heterogeneous and sometimes change domains, schemas or access policy.
2. **Data.gov API uncertainty:** the legacy CKAN endpoint is unavailable; the project does not scrape the public website as a substitute.
3. **Credentialed federal sources:** Census and Congress.gov require optional API keys for the current adapters.
4. **Search is not analysis:** current state tools discover datasets but do not yet normalize comparable indicators across states.
5. **Geography is incomplete:** state-level resolution is present; county and finer Census geography are next.
6. **Coverage is curated, not national:** five state packs are a representative foundation, not a claim of all-state coverage.

---

## 8. Next build priority

The next high-value slice is a **climate/environment vertical workflow** across federal and state sources:

- add NOAA/EPA federal adapters;
- identify stable environmental datasets in each curated state portal;
- add freshness, licence and dataset-quality metadata;
- add higher-level tools such as `find_state_environment_data` and `compare_state_sources`;
- extend geography to counties and Census areas;
- keep raw upstream payloads available behind normalized fields.

This will test whether the gateway can answer a genuinely cross-jurisdiction question rather than merely expose independent catalogue wrappers.

---

## Citations and licence

This document describes software verification results and links to official upstream APIs and portals. It is a test artefact for OpenUSPublicDataMCP, not an official publication of the US Government or any state government. Upstream licensing and attribution requirements must be checked per dataset before redistribution.
