export type ExplorerLayer = {
  id: "states" | "curated-portals" | "federal-sources";
  category: string;
  label: string;
  jurisdiction: string;
  geometry: "point" | "non_spatial";
  default_enabled: boolean;
  coverage_status: string;
  source_id: string;
};

export type MapEntity = {
  id: string;
  type: "state";
  title: string;
  latitude: number;
  longitude: number;
  observed_at: string | null;
  severity: string | null;
  properties: {
    fips: string;
    coverage_status: "curated_portal" | "registry_only";
    curated_portal: StatePortal | null;
  };
};

export type StatePortal = {
  state_code: string;
  state: string;
  platform: string;
  base_url: string;
  official: boolean;
  notes: string | null;
};

export type Source = {
  name: string;
  url: string;
  official: boolean;
  jurisdiction: string;
  auth: string;
  licence: string;
  platform?: string | null;
  status?: string | null;
};

export const BASEMAPS = {
  dark: {
    label: "Dark",
    url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
  },
  light: {
    label: "Light",
    url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
  },
  osm: {
    label: "OpenStreetMap",
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  },
} as const;

export type BasemapId = keyof typeof BASEMAPS;

export type ExplorerCounts = {
  states: number;
  curated: number;
  sources: number;
};

export function groupLayers(layers: ExplorerLayer[]): Array<[string, ExplorerLayer[]]> {
  const grouped = new Map<string, ExplorerLayer[]>();
  for (const layer of layers) grouped.set(layer.category, [...(grouped.get(layer.category) || []), layer]);
  return [...grouped.entries()];
}

export function initialLayerState(layers: ExplorerLayer[]): Record<string, boolean> {
  return Object.fromEntries(layers.map((layer) => [layer.id, layer.default_enabled]));
}

export function layerCount(layerId: ExplorerLayer["id"], counts: ExplorerCounts): number {
  if (layerId === "states") return counts.states;
  if (layerId === "curated-portals") return counts.curated;
  return counts.sources;
}

export function markerRadius(active: boolean, curated: boolean): number {
  if (active) return 12;
  if (curated) return 9;
  return 6;
}

export function markerStyle(curated: boolean) {
  return curated
    ? { color: "#047857", fillColor: "#34d399", fillOpacity: 0.82, weight: 2 }
    : { color: "#1e3a5f", fillColor: "#60a5fa", fillOpacity: 0.62, weight: 1.5 };
}
