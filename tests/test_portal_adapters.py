import httpx
import respx

from openuspublicdata_mcp.adapters.portals import query_arcgis, query_socrata, search_ckan, search_socrata


@respx.mock
def test_search_socrata_uses_catalogue_api():
    route = respx.get("https://api.us.socrata.com/api/catalog/v1").mock(return_value=httpx.Response(200, json={"results": [{"resource": {"name": "Test"}}]}))
    result = search_socrata("transport", 5)
    assert route.called
    assert result["results"][0]["resource"]["name"] == "Test"


@respx.mock
def test_query_socrata_returns_rows():
    route = respx.get("https://data.example.gov/resource/abcd-1234.json").mock(return_value=httpx.Response(200, json=[{"id": 1}]))
    result = query_socrata("data.example.gov", "abcd-1234", 10)
    assert route.called
    assert result == [{"id": 1}]


@respx.mock
def test_query_arcgis_adds_query_suffix():
    route = respx.get("https://gis.example.gov/arcgis/rest/services/Test/FeatureServer/0/query").mock(return_value=httpx.Response(200, json={"features": []}))
    result = query_arcgis("https://gis.example.gov/arcgis/rest/services/Test/FeatureServer/0")
    assert route.called
    assert result["features"] == []


@respx.mock
def test_search_ckan_uses_instance_api():
    route = respx.get("https://data.example.gov/api/3/action/package_search").mock(return_value=httpx.Response(200, json={"success": True, "result": {"count": 0}}))
    result = search_ckan("https://data.example.gov", "housing")
    assert route.called
    assert result["result"]["count"] == 0
