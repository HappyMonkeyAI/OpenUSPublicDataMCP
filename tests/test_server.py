from openuspublicdata_mcp.server import get_census_state_population, health_check, list_federal_agencies, list_public_data_sources


def test_health_check():
    result = health_check()
    assert result["status"] == "ok"
    assert result["source_count"] >= 2


def test_source_listing_has_provenance():
    result = list_public_data_sources()
    assert result["source"]["name"] == "OpenUSPublicDataMCP source registry"
    assert all("jurisdiction" in item for item in result["data"])


def test_census_state_population_rejects_unsupported_year():
    try:
        get_census_state_population(2023)
    except ValueError as exc:
        assert "between 2009 and 2022" in str(exc)
    else:
        raise AssertionError("expected ValueError")
