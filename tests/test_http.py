import httpx
import respx

from openuspublicdata_mcp.http import request_json


@respx.mock
def test_request_json_retries_transient_status():
    route = respx.get("https://example.test/data").mock(
        side_effect=[httpx.Response(503), httpx.Response(200, json={"ok": True})]
    )
    result = request_json("GET", "https://example.test/data", retries=1)
    assert result == {"ok": True}
    assert route.call_count == 2
