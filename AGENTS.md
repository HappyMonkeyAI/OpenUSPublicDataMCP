# AGENTS — OpenUSPublicDataMCP

## First actions

1. Read `CONTEXT.md`, `HERMES.md`, and relevant ADRs.
2. Check the task board with `python3 scripts/tasks.py list` when present.
3. Keep one source adapter or contract change per focused slice.

## Build rules

- Federal-first; do not claim complete US coverage.
- Prefer official APIs and bulk data over scraping.
- Core tools must work without credentials where practical.
- Optional API keys must be documented and must not break startup.
- Every returned result includes source and retrieval metadata.
- Never log secrets or write `.env` files to git.
- Stdio MCP output belongs exclusively to the protocol.

## Verification

```bash
pytest
python -m compileall src tests
fastmcp inspect src/openuspublicdata_mcp/server.py:mcp
fastmcp list src/openuspublicdata_mcp/server.py --json
```
