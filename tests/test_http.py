import httpx
import pytest
import respx
from unittest.mock import patch

from openuspublicdata_mcp.http import request_json


@respx.mock
def test_request_json_retries_transient_status():
    route = respx.get("https://example.test/data").mock(
        side_effect=[httpx.Response(503), httpx.Response(200, json={"ok": True})]
    )
    with patch("time.sleep") as mock_sleep:
        result = request_json("GET", "https://example.test/data", retries=1)
        assert result == {"ok": True}
        assert route.call_count == 2
        mock_sleep.assert_called_once_with(0.2)


@respx.mock
def test_request_json_redacts_api_keys_on_failure():
    route = respx.get("https://example.test/secure").mock(
        return_value=httpx.Response(400)
    )
    with pytest.raises(Exception) as excinfo:
        request_json("GET", "https://example.test/secure", params={"key": "supersecretkey", "other": "public"}, retries=0)
    
    msg = str(excinfo.value)
    assert "supersecretkey" not in msg
    assert "REDACTED" in msg
    assert "public" in msg


@respx.mock
def test_request_json_retries_connection_error():
    route = respx.get("https://example.test/data").mock(
        side_effect=[httpx.ConnectError("Connection failed"), httpx.Response(200, json={"ok": True})]
    )
    with patch("time.sleep") as mock_sleep:
        result = request_json("GET", "https://example.test/data", retries=1)
        assert result == {"ok": True}
        assert route.call_count == 2
        mock_sleep.assert_called_once_with(0.2)


@respx.mock
def test_request_json_no_sleep_on_final_failure():
    route = respx.get("https://example.test/data").mock(
        return_value=httpx.Response(500)
    )
    with patch("time.sleep") as mock_sleep:
        with pytest.raises(httpx.HTTPStatusError):
            request_json("GET", "https://example.test/data", retries=2)
        assert route.call_count == 3
        # Should sleep after attempt 0 (0.2) and attempt 1 (0.4), but NOT after attempt 2.
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(0.2)
        mock_sleep.assert_any_call(0.4)

