import httpx
import respx

from openuspublicdata_mcp.server import search_data_gov


@respx.mock
def test_search_data_gov_normalizes_catalogue_response():
    route = respx.get("https://catalog.data.gov/api/3/action/package_search").mock(
        return_value=httpx.Response(200, json={"success": True, "result": {"count": 1, "results": [{"title": "Example"}]}})
    )
    result = search_data_gov("climate", limit=5)
    assert route.called
    assert result["data"]["count"] == 1
    assert result["source"]["official"] is True
