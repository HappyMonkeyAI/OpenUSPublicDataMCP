# OpenUSPublicDataMCP Bootstrap Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a federal-first MCP gateway for high-value US public data, then expand through reusable state/local portal adapters.

**Architecture:** FastMCP tools call thin official-source adapters and return a common provenance envelope. Jurisdiction and platform metadata are first-class so federal, state, county and city sources are not falsely conflated.

**Tech Stack:** Python 3.11+, FastMCP, httpx, pytest, respx.

**Q2 status:** Phases 1, 3, 4 and 5 are complete in the current foundation. Phase 2 federal breadth and the climate/environment vertical remain next.

---

### Phase 1: Federal foundations

- Stabilise source registry and response contract.
- Add Data.gov catalogue search and dataset retrieval.
- Add Census geography/profile adapter (optional key).
- Add Congress.gov search adapter (optional API key).
- Add Federal Register search adapter.
- Add USAspending agency and award/search adapters.
- Add reusable Socrata, ArcGIS REST and CKAN platform adapters.
- Add live smoke commands and fixtures.

### Phase 2: Federal breadth

- Add BLS, BEA, NOAA, EPA, FDA, CDC and USDA adapters where API contracts are clear.
- Classify authentication and rate limits per source.
- Add source health/availability metadata without making optional providers fatal.

### Phase 3: State/local platform adapters

- Implement Socrata discovery/query adapter.
- Implement ArcGIS REST feature-service adapter.
- Implement CKAN catalogue adapter.
- Add jurisdiction registry and selected state packs.
- Add local portal discovery; do not promise full local coverage.

### Phase 4: Core hardening and geography

- Use shared bounded HTTP retries and typed source metadata.
- Resolve state names/abbreviations to state FIPS codes.
- Add registry filtering by jurisdiction and platform.
- Extend geography to counties, congressional districts and Census geographies.

### Phase 5: Curated state packs

- California: CKAN
- New York, Texas and Washington: Socrata
- Florida: ArcGIS Hub search
- Add state-specific dataset fixtures and freshness/licence notes.

### Phase 6: USA web discovery explorer

**Goal:** Add a React/Leaflet discovery map that exposes federal sources, all state/FIPS geography, and curated state portals without implying uniform national dataset coverage.

#### Task 6.1 — Explorer contracts and REST surface

- **Create:** `src/openuspublicdata_mcp/explorer.py`, `tests/test_explorer.py`
- **Modify:** `src/openuspublicdata_mcp/http_server.py`, `pyproject.toml`
- **Contract:** normalized state map entities, typed layer/source catalogue, source search, and state portal metadata with jurisdiction/auth/licence preserved.
- **TDD:** focused API tests fail before routes and normalizers are implemented.

#### Task 6.2 — React/Leaflet map

- **Create:** `web/` Vite application and `scripts/run-web.sh`
- **Behavior:** US state centroid markers, curated-portal highlighting, category/layer controls, source status/counts, federal/state-local discovery search, state detail panel, and attribution-aware dark/light/OSM basemaps.
- **Constraint:** discovery explorer only; do not fabricate live point layers or claim complete state/local coverage.
- **TDD:** pure layer/state helpers get Vitest coverage before UI wiring.

#### Task 6.3 — Documentation and verification

- **Modify:** `README.md`, `CONTEXT.md`
- **Create:** `web/README.md`, `research/notes/openus-map-explorer.md`
- **Verify:** full pytest, compileall, FastMCP inspect/list, Vitest, Vite production build, REST HTTP probes, and browser visual/interaction smoke.

---

### Verification gates

```bash
pytest
python -m compileall src tests
fastmcp inspect src/openuspublicdata_mcp/server.py:mcp
fastmcp list src/openuspublicdata_mcp/server.py --json
fastmcp call src/openuspublicdata_mcp/server.py search_data_gov query='climate' limit=3 --json
```
