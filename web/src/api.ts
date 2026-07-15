import type { ExplorerLayer, MapEntity, Source } from "./layers";

const API = "/api/explorer";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API}${path}`);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
  return response.json() as Promise<T>;
}

export function fetchCatalogue() {
  return getJson<{
    layers: ExplorerLayer[];
    layer_count: number;
    state_count: number;
    curated_state_count: number;
    source_count: number;
  }>("/catalogue");
}

export function fetchStates() {
  return getJson<{ count: number; entities: MapEntity[] }>("/states");
}

export function fetchState(code: string) {
  return getJson<Record<string, unknown>>(`/states/${encodeURIComponent(code)}`);
}

export function fetchSources(query = "") {
  return getJson<{ query: string; count: number; sources: Source[] }>(
    `/sources?q=${encodeURIComponent(query)}`,
  );
}
