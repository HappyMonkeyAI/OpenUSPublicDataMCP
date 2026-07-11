import httpx
import respx

from openuspublicdata_mcp.server import list_curated_state_portals, search_state_data
from openuspublicdata_mcp.state_portals import list_state_portals


def test_curated_state_pack_contains_selected_states():
    assert {item["state_code"] for item in list_state_portals()} == {"CA", "NY", "TX", "WA", "FL"}
    result = list_curated_state_portals()
    assert result["source"]["jurisdiction"] == "state_or_local"


@respx.mock
def test_state_search_dispatches_to_california_ckan():
    route = respx.get("https://data.ca.gov/api/3/action/package_search").mock(
        return_value=httpx.Response(200, json={"success": True, "result": {"count": 1}})
    )
    result = search_state_data("CA", "climate", 2)
    assert route.called
    assert result["source"]["platform"] == "ckan"
    assert result["data"]["result"]["count"] == 1
