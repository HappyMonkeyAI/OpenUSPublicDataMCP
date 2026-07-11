import pytest

from openuspublicdata_mcp.geography import resolve_state


def test_resolve_state_by_name():
    assert resolve_state("Texas") == {
        "query": "Texas",
        "state": "Texas",
        "state_code": "TX",
        "state_fips": "48",
        "jurisdiction_level": "state",
    }


def test_resolve_state_from_city_string():
    result = resolve_state("Austin, Texas")
    assert result["state_code"] == "TX"
    assert result["state_fips"] == "48"


def test_resolve_state_rejects_unknown_location():
    with pytest.raises(ValueError, match="could not resolve"):
        resolve_state("London")
