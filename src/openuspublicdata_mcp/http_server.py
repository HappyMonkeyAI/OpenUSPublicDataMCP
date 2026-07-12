from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from openuspublicdata_mcp.explorer import (
    explorer_catalogue,
    search_registered_sources,
    state_detail,
    state_entities,
)
from openuspublicdata_mcp.server import health_check, mcp

mcp_app = mcp.http_app()
app = FastAPI(title="OpenUSPublicDataMCP HTTP", version="0.1.0", lifespan=mcp_app.lifespan)
REPO_ROOT = Path(__file__).resolve().parents[2]
WEB_DIST = REPO_ROOT / "web" / "dist"


@app.get("/health")
def health() -> dict[str, object]:
    return health_check()


@app.get("/api/explorer/catalogue")
def api_explorer_catalogue() -> dict[str, object]:
    return explorer_catalogue()


@app.get("/api/explorer/states")
def api_explorer_states() -> dict[str, object]:
    entities = state_entities()
    return {"count": len(entities), "entities": entities}


@app.get("/api/explorer/states/{state_code}")
def api_explorer_state(state_code: str) -> dict[str, object]:
    try:
        return state_detail(state_code)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="state_not_found") from exc


@app.get("/api/explorer/sources")
def api_explorer_sources(q: str = Query("", max_length=120)) -> dict[str, object]:
    sources = search_registered_sources(q)
    return {"query": q.strip(), "count": len(sources), "sources": sources}


if WEB_DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=WEB_DIST / "assets"), name="explorer-assets")

    @app.get("/")
    def explorer_root() -> FileResponse:
        return FileResponse(WEB_DIST / "index.html")


app.mount("/", mcp_app)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "openuspublicdata_mcp.http_server:app",
        host=os.getenv("OPENUS_HOST", "127.0.0.1"),
        port=int(os.getenv("OPENUS_PORT", "8787")),
        reload=False,
    )


if __name__ == "__main__":
    main()
