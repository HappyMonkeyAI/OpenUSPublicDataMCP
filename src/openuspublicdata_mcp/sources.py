from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    official: bool
    jurisdiction: str
    auth: str
    licence: str | None = None


SOURCES = {
    "data_gov": Source("Data.gov", "https://data.gov/", True, "federal", "none", "US Government open data terms"),
    "census": Source("US Census Bureau", "https://api.census.gov/data.html", True, "federal", "optional_key", "US Government public data"),
    "usaspending": Source("USAspending.gov", "https://api.usaspending.gov/", True, "federal", "none", "US Government public data"),
    "federal_register": Source("Federal Register", "https://www.federalregister.gov/developers/documentation/api/v1", True, "federal", "none", "US Government public data"),
    "congress": Source("Congress.gov API", "https://api.congress.gov/", True, "federal", "optional_key", "US Government public data"),
    "socrata": Source("Socrata catalog", "https://api.us.socrata.com/api/catalog/v1", False, "state_or_local", "none", "Licence varies by dataset"),
    "arcgis": Source("ArcGIS REST feature services", "https://developers.arcgis.com/rest/services-reference/", False, "state_or_local", "none", "Licence varies by service"),
    "ckan": Source("CKAN catalogues", "https://docs.ckan.org/en/latest/api/", False, "state_or_local", "none", "Licence varies by dataset"),
}


def list_sources() -> list[dict[str, object]]:
    return [asdict(source) for source in SOURCES.values()]
