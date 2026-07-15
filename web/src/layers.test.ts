import { describe, expect, it } from "vitest";

import {
  BASEMAPS,
  groupLayers,
  initialLayerState,
  layerCount,
  markerRadius,
  markerStyle,
  type ExplorerLayer,
} from "./layers";

const layers: ExplorerLayer[] = [
  {
    id: "states",
    category: "Geography",
    label: "States + DC",
    jurisdiction: "state",
    geometry: "point",
    default_enabled: true,
    coverage_status: "national_reference",
    source_id: "census",
  },
  {
    id: "curated-portals",
    category: "State & local",
    label: "Curated state portals",
    jurisdiction: "state",
    geometry: "point",
    default_enabled: true,
    coverage_status: "selected_states",
    source_id: "state_portal_registry",
  },
];

describe("US explorer layer helpers", () => {
  it("groups layers in catalogue order", () => {
    expect(groupLayers(layers)).toEqual([
      ["Geography", [layers[0]]],
      ["State & local", [layers[1]]],
    ]);
  });

  it("initialises enabled state from the server catalogue", () => {
    expect(initialLayerState(layers)).toEqual({ states: true, "curated-portals": true });
  });

  it("distinguishes curated states and exposes attributed basemaps", () => {
    expect(markerStyle(true).fillColor).not.toBe(markerStyle(false).fillColor);
    expect(Object.keys(BASEMAPS)).toEqual(["dark", "light", "osm"]);
    expect(BASEMAPS.osm.attribution).toContain("OpenStreetMap");
  });

  it("calculates layer counts without nested conditionals", () => {
    const counts = { states: 51, curated: 5, sources: 12 };

    expect(layerCount("states", counts)).toBe(51);
    expect(layerCount("curated-portals", counts)).toBe(5);
    expect(layerCount("federal-sources", counts)).toBe(12);
  });

  it("prioritises active marker size over curated marker size", () => {
    expect(markerRadius(true, true)).toBe(12);
    expect(markerRadius(false, true)).toBe(9);
    expect(markerRadius(false, false)).toBe(6);
  });
});
