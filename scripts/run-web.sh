#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export OPENUS_PORT="${OPENUS_PORT:-8787}"
if [[ ! -d web/node_modules ]]; then
  (cd web && npm install)
fi
(cd web && npm run build)
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
echo "OpenUS API + explorer: http://127.0.0.1:${OPENUS_PORT}"
exec .venv/bin/python -m openuspublicdata_mcp.http_server
