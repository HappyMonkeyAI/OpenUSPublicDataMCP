# OpenUS map explorer implementation note

## Pattern adopted

The OpenUK explorer's React/Leaflet discovery shape was selectively ported: typed layer catalogue, source counts/status, attribution-aware basemaps, normalized map entities, and a source/detail panel.

## US-specific adaptation

- All 50 states plus DC are represented by approximate label centroids with Census-style state FIPS identity.
- CA, NY, TX, WA and FL are highlighted only because this repository has curated official portal records for them.
- Federal and state/local registry entries preserve jurisdiction, authentication, platform, licence and availability status.
- Source search filters the local registry and does not imply that upstream datasets have been queried.

## Boundaries

- Centroids are navigation aids, not analytical state boundaries.
- Registry-only states are labelled honestly.
- No live incident, climate or spending points are fabricated from non-spatial source responses.
- Future spatial layers require a typed provider adapter, realistic fixture, source metadata and live smoke evidence.

## Files

- Backend contract: `src/openuspublicdata_mcp/explorer.py`
- REST/static host: `src/openuspublicdata_mcp/http_server.py`
- Frontend: `web/`
- Verification: `tests/test_explorer.py`, `web/src/layers.test.ts`
