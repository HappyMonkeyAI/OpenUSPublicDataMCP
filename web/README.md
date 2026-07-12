# OpenUS Public Data Explorer

React + Leaflet discovery UI served by `openuspublicdata_mcp.http_server`.

## Features

- All 50 states plus DC using approximate label centroids and state FIPS metadata.
- Clear distinction between registry-only geography and the five curated official state portals.
- Searchable federal/state-local source registry with jurisdiction, auth, platform and status.
- Config-driven discovery layers and source counts.
- CARTO dark/light and OpenStreetMap basemaps with attribution.
- Explicit discovery boundary: no fabricated live markers or claim of complete US coverage.

## Production-style run

```bash
cd /home/stephen/projects/OpenUSPublicDataMCP
./scripts/run-web.sh
```

Open `http://127.0.0.1:8787`. MCP remains at `/mcp`; health is at `/health`.

## Development

Terminal 1:

```bash
PYTHONPATH=src OPENUS_PORT=8787 .venv/bin/python -m openuspublicdata_mcp.http_server
```

Terminal 2:

```bash
cd web
npm install
npm run dev
```

Vite uses port 5174 and proxies `/api` and `/health` to 8787.

## Verification

```bash
cd web
npm test
npm run build
```
