import httpx
import respx

from openuspublicdata_mcp.server import search_federal_register, search_usaspending_awards


@respx.mock
def test_search_federal_register_returns_documents():
    route = respx.get("https://www.federalregister.gov/api/v1/documents.json").mock(
        return_value=httpx.Response(200, json={"count": 1, "results": [{"title": "Climate notice"}]})
    )
    result = search_federal_register("climate", limit=5)
    assert route.called
    assert result["data"]["results"][0]["title"] == "Climate notice"
    assert result["source"]["official"] is True


@respx.mock
def test_search_usaspending_awards_posts_filters():
    route = respx.post("https://api.usaspending.gov/api/v2/search/spending_by_award/").mock(
        return_value=httpx.Response(200, json={"results": [{"Award ID": "A-1"}]})
    )
    result = search_usaspending_awards("climate", limit=5)
    assert route.called
    assert route.calls[0].request.content
    assert result["data"]["results"][0]["Award ID"] == "A-1"
    assert result["source"]["name"] == "USAspending.gov"
