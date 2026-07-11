# OpenUSPublicDataMCP Bootstrap Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a federal-first MCP gateway for high-value US public data, then expand through reusable state/local portal adapters.

**Architecture:** FastMCP tools call thin official-source adapters and return a common provenance envelope. Jurisdiction and platform metadata are first-class so federal, state, county and city sources are not falsely conflated.

**Tech Stack:** Python 3.11+, FastMCP, httpx, pytest, respx.

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

### Verification gates

```bash
pytest
python -m compileall src tests
fastmcp inspect src/openuspublicdata_mcp/server.py:mcp
fastmcp list src/openuspublicdata_mcp/server.py --json
fastmcp call src/openuspublicdata_mcp/server.py search_data_gov query='climate' limit=3 --json
```
