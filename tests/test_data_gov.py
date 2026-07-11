import httpx
import respx

from openuspublicdata_mcp.server import list_federal_agencies, search_data_gov


@respx.mock
def test_search_data_gov_normalizes_catalogue_response():
    route = respx.get("https://catalog.data.gov/api/3/action/package_search").mock(
        return_value=httpx.Response(200, json={"success": True, "result": {"count": 1, "results": [{"title": "Example"}]}})
    )
    result = search_data_gov("climate", limit=5)
    assert route.called
    assert result["data"]["count"] == 1
    assert result["source"]["official"] is True


@respx.mock
def test_list_federal_agencies_preserves_source_metadata():
    route = respx.get("https://api.usaspending.gov/api/v2/references/toptier_agencies/").mock(
        return_value=httpx.Response(200, json={"results": [{"agency_name": "Example"}]})
    )
    result = list_federal_agencies()
    assert route.called
    assert result["data"]["results"][0]["agency_name"] == "Example"
    assert result["source"]["name"] == "USAspending.gov"
