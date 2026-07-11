from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .adapters.portals import search_arcgis_portal, search_ckan, search_socrata
from .geography import resolve_state


@dataclass(frozen=True)
class StatePortal:
    state_code: str
    state: str
    platform: str
    base_url: str
    official: bool = True
    notes: str | None = None


STATE_PORTALS = {
    "CA": StatePortal("CA", "California", "ckan", "https://data.ca.gov"),
    "NY": StatePortal("NY", "New York", "socrata", "https://data.ny.gov"),
    "TX": StatePortal("TX", "Texas", "socrata", "https://data.texas.gov"),
    "WA": StatePortal("WA", "Washington", "socrata", "https://data.wa.gov"),
    "FL": StatePortal("FL", "Florida", "arcgis", "https://flgio.maps.arcgis.com", notes="Florida Geospatial Open Data Portal"),
}


def list_state_portals() -> list[dict[str, Any]]:
    return [asdict(portal) for portal in STATE_PORTALS.values()]


def get_state_portal(state: str) -> StatePortal:
    code = resolve_state(state)["state_code"]
    try:
        return STATE_PORTALS[code]
    except KeyError as exc:
        raise ValueError(f"no curated state portal is registered for {code}") from exc


def search_state_portal(state: str, query: str, limit: int = 10) -> tuple[StatePortal, Any]:
    portal = get_state_portal(state)
    if portal.platform == "ckan":
        data = search_ckan(portal.base_url, query, limit)
    elif portal.platform == "socrata":
        data = search_socrata(query, limit, domain=portal.base_url.removeprefix("https://"))
    elif portal.platform == "arcgis":
        data = search_arcgis_portal(portal.base_url, query, limit)
    else:
        raise ValueError(f"unsupported state portal platform: {portal.platform}")
    return portal, data
