import httpx
import pytest
import respx

from openuspublicdata_mcp.server import search_congress_bills, get_census_state_population


def test_census_requires_key_when_upstream_redirects_to_missing_key(monkeypatch):
    monkeypatch.delenv("CENSUS_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="CENSUS_API_KEY"):
        get_census_state_population()


def test_congress_requires_api_key(monkeypatch):
    monkeypatch.delenv("CONGRESS_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="CONGRESS_API_KEY"):
        search_congress_bills("climate")


@respx.mock
def test_congress_bills_uses_api_key(monkeypatch):
    monkeypatch.setenv("CONGRESS_API_KEY", "test-key")
    route = respx.get("https://api.congress.gov/v3/bill").mock(
        return_value=httpx.Response(200, json={"bills": [{"number": "1"}]})
    )
    result = search_congress_bills("climate", limit=3)
    assert route.called
    assert route.calls[0].request.url.params["api_key"] == "test-key"
    assert result["data"]["bills"][0]["number"] == "1"
