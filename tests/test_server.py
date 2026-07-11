from openuspublicdata_mcp.server import health_check, list_public_data_sources


def test_health_check():
    result = health_check()
    assert result["status"] == "ok"
    assert result["source_count"] >= 2


def test_source_listing_has_provenance():
    result = list_public_data_sources()
    assert result["source"]["name"] == "OpenUSPublicDataMCP source registry"
    assert all("jurisdiction" in item for item in result["data"])
