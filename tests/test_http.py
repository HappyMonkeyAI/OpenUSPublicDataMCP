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


@respx.mock
def test_request_json_redacts_api_keys_on_failure():
    route = respx.get("https://example.test/secure").mock(
        return_value=httpx.Response(400)
    )
    import pytest
    with pytest.raises(Exception) as excinfo:
        request_json("GET", "https://example.test/secure", params={"key": "supersecretkey", "other": "public"}, retries=0)
    
    msg = str(excinfo.value)
    assert "supersecretkey" not in msg
    assert "REDACTED" in msg
    assert "public" in msg
