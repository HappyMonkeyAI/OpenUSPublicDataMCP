"""Static, source-cited discovery metadata for the US web explorer."""

from __future__ import annotations

from typing import Any

from .geography import STATES
from .sources import list_sources
from .state_portals import STATE_PORTALS

# Approximate state label centroids for discovery navigation, not analytical geometry.
STATE_CENTROIDS: dict[str, tuple[float, float]] = {
    "AL": (32.8067, -86.7911), "AK": (61.3707, -152.4044), "AZ": (33.7298, -111.4312),
    "AR": (34.9697, -92.3731), "CA": (36.1162, -119.6816), "CO": (39.0598, -105.3111),
    "CT": (41.5978, -72.7554), "DE": (39.3185, -75.5071), "FL": (27.7663, -81.6868),
    "GA": (33.0406, -83.6431), "HI": (21.0943, -157.4983), "ID": (44.2405, -114.4788),
    "IL": (40.3495, -88.9861), "IN": (39.8494, -86.2583), "IA": (42.0115, -93.2105),
    "KS": (38.5266, -96.7265), "KY": (37.6681, -84.6701), "LA": (31.1695, -91.8678),
    "ME": (44.6939, -69.3819), "MD": (39.0639, -76.8021), "MA": (42.2302, -71.5301),
    "MI": (43.3266, -84.5361), "MN": (45.6945, -93.9002), "MS": (32.7416, -89.6787),
    "MO": (38.4561, -92.2884), "MT": (46.9219, -110.4544), "NE": (41.1254, -98.2681),
    "NV": (38.3135, -117.0554), "NH": (43.4525, -71.5639), "NJ": (40.2989, -74.5210),
    "NM": (34.8405, -106.2485), "NY": (42.1657, -74.9481), "NC": (35.6301, -79.8064),
    "ND": (47.5289, -99.7840), "OH": (40.3888, -82.7649), "OK": (35.5653, -96.9289),
    "OR": (44.5720, -122.0709), "PA": (40.5908, -77.2098), "RI": (41.6809, -71.5118),
    "SC": (33.8569, -80.9450), "SD": (44.2998, -99.4388), "TN": (35.7478, -86.6923),
    "TX": (31.0545, -97.5635), "UT": (40.1500, -111.8624), "VT": (44.0459, -72.7107),
    "VA": (37.7693, -78.1700), "WA": (47.4009, -121.4905), "WV": (38.4912, -80.9545),
    "WI": (44.2685, -89.6165), "WY": (42.7560, -107.3025), "DC": (38.9072, -77.0369),
}

EXPLORER_LAYERS: tuple[dict[str, Any], ...] = (
    {
        "id": "states", "category": "Geography", "label": "States + DC",
        "jurisdiction": "state", "geometry": "point", "default_enabled": True,
        "coverage_status": "national_reference", "source_id": "census",
    },
    {
        "id": "curated-portals", "category": "State & local", "label": "Curated state portals",
        "jurisdiction": "state", "geometry": "point", "default_enabled": True,
        "coverage_status": "selected_states", "source_id": "state_portal_registry",
    },
    {
        "id": "federal-sources", "category": "Federal", "label": "Federal source catalogue",
        "jurisdiction": "federal", "geometry": "non_spatial", "default_enabled": True,
        "coverage_status": "registered_sources", "source_id": "source_registry",
    },
)


def state_detail(code: str) -> dict[str, Any]:
    code = code.upper()
    if code not in STATES:
        raise KeyError(code)
    name, fips = STATES[code]
    portal = STATE_PORTALS.get(code)
    portal_data = None
    if portal:
        portal_data = {
            "state_code": portal.state_code,
            "state": portal.state,
            "platform": portal.platform,
            "base_url": portal.base_url,
            "official": portal.official,
            "notes": portal.notes,
        }
    return {
        "state_code": code,
        "state": name,
        "state_fips": fips,
        "curated_portal": portal_data,
        "coverage_status": "curated_portal" if portal else "registry_only",
    }


def state_entities() -> list[dict[str, Any]]:
    missing_centroids = sorted(STATES.keys() - STATE_CENTROIDS.keys())
    if missing_centroids:
        missing = ", ".join(missing_centroids)
        raise ValueError(f"Missing centroids for states: {missing}")

    entities = []
    for code, (name, fips) in STATES.items():
        latitude, longitude = STATE_CENTROIDS[code]
        detail = state_detail(code)
        entities.append({
            "id": code,
            "type": "state",
            "title": name,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "observed_at": None,
            "severity": None,
            "properties": {
                "fips": fips,
                "coverage_status": detail["coverage_status"],
                "curated_portal": detail["curated_portal"],
            },
        })
    return entities


def explorer_catalogue() -> dict[str, Any]:
    return {
        "layers": list(EXPLORER_LAYERS),
        "layer_count": len(EXPLORER_LAYERS),
        "state_count": len(STATES),
        "curated_state_count": len(STATE_PORTALS),
        "source_count": len(list_sources()),
    }


def search_registered_sources(query: str = "") -> list[dict[str, object]]:
    value = query.strip().lower()
    sources = list_sources()
    if not value:
        return sources
    keys = ("name", "url", "jurisdiction", "auth", "licence", "platform", "status")
    return [
        source for source in sources
        if any(value in str(source.get(key, "")).lower() for key in keys)
    ]
