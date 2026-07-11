from __future__ import annotations

from .models import Source


SOURCES = {
    "data_gov": Source("Data.gov", "https://data.gov/", True, "federal", "none", "US Government open data terms", "catalogue", "deferred_api"),
    "census": Source("US Census Bureau", "https://api.census.gov/data.html", True, "federal", "optional_key", "US Government public data"),
    "usaspending": Source("USAspending.gov", "https://api.usaspending.gov/", True, "federal", "none", "US Government public data"),
    "federal_register": Source("Federal Register", "https://www.federalregister.gov/developers/documentation/api/v1", True, "federal", "none", "US Government public data"),
    "congress": Source("Congress.gov API", "https://api.congress.gov/", True, "federal", "optional_key", "US Government public data"),
    "socrata": Source("Socrata catalog", "https://api.us.socrata.com/api/catalog/v1", False, "state_or_local", "none", "Licence varies by dataset", "socrata"),
    "arcgis": Source("ArcGIS REST feature services", "https://developers.arcgis.com/rest/services-reference/", False, "state_or_local", "none", "Licence varies by service", "arcgis"),
    "ckan": Source("CKAN catalogues", "https://docs.ckan.org/en/latest/api/", False, "state_or_local", "none", "Licence varies by dataset", "ckan"),
}


def list_sources() -> list[dict[str, object]]:
    return [source.as_dict() for source in SOURCES.values()]


def find_sources(jurisdiction: str | None = None, platform: str | None = None) -> list[dict[str, object]]:
    result = list_sources()
    if jurisdiction:
        result = [item for item in result if item["jurisdiction"] == jurisdiction]
    if platform:
        result = [item for item in result if item["platform"] == platform]
    return result
