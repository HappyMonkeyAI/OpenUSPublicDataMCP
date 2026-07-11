from __future__ import annotations

import os

from fastapi import FastAPI

from openuspublicdata_mcp.server import health_check, mcp

mcp_app = mcp.http_app()
app = FastAPI(title="OpenUSPublicDataMCP HTTP", version="0.1.0", lifespan=mcp_app.lifespan)


@app.get("/health")
def health() -> dict[str, object]:
    return health_check()


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
