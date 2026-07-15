import { useEffect, useMemo, useState } from "react";
import { CircleMarker, MapContainer, Popup, TileLayer, useMap } from "react-leaflet";

import { fetchCatalogue, fetchSources, fetchState, fetchStates } from "./api";
import {
  BASEMAPS,
  groupLayers,
  initialLayerState,
  layerCount,
  markerRadius,
  markerStyle,
  type BasemapId,
  type ExplorerCounts,
  type ExplorerLayer,
  type MapEntity,
  type Source,
} from "./layers";

const US_CENTER: [number, number] = [39.4, -98.5];

function MapFocus({ entity }: { entity: MapEntity | null }) {
  const map = useMap();
  useEffect(() => {
    if (entity) map.flyTo([entity.latitude, entity.longitude], entity.id === "AK" || entity.id === "HI" ? 5 : 6);
  }, [entity, map]);
  return null;
}

type DiscoveryLayersProps = {
  layers: ExplorerLayer[];
  enabled: Record<string, boolean>;
  counts: ExplorerCounts;
  onToggle: (layerId: ExplorerLayer["id"]) => void;
};

function DiscoveryLayers({ layers, enabled, counts, onToggle }: DiscoveryLayersProps) {
  return groupLayers(layers).map(([category, entries]) => (
    <details open key={category}>
      <summary>{category}</summary>
      {entries.map((layer) => (
        <label className="layer-row" key={layer.id}>
          <input type="checkbox" checked={enabled[layer.id] || false} onChange={() => onToggle(layer.id)} />
          <span className={`dot ${layer.id}`} />
          <span><strong>{layer.label}</strong><small>{layer.coverage_status.replace(/_/g, " ")}</small></span>
          <b>{layerCount(layer.id, counts)}</b>
        </label>
      ))}
    </details>
  ));
}

type StateMarkerProps = {
  entity: MapEntity;
  curatedLayerEnabled: boolean;
  active: boolean;
  onSelect: (entity: MapEntity) => void;
};

function StateMarker({ entity, curatedLayerEnabled, active, onSelect }: StateMarkerProps) {
  const curated = Boolean(entity.properties.curated_portal) && curatedLayerEnabled;
  const style = markerStyle(curated);

  return (
    <CircleMarker
      center={[entity.latitude, entity.longitude]}
      eventHandlers={{ click: () => onSelect(entity) }}
      pathOptions={{ ...style, weight: active ? 4 : style.weight }}
      radius={markerRadius(active, curated)}
    >
      <Popup><strong>{entity.title}</strong><br />FIPS {entity.properties.fips}<br />{entity.properties.curated_portal ? `${entity.properties.curated_portal.platform.toUpperCase()} portal registered` : "Registry geography only"}</Popup>
    </CircleMarker>
  );
}

export default function App() {
  const [layers, setLayers] = useState<ExplorerLayer[]>([]);
  const [enabled, setEnabled] = useState<Record<string, boolean>>({});
  const [states, setStates] = useState<MapEntity[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [selected, setSelected] = useState<MapEntity | null>(null);
  const [stateDetail, setStateDetail] = useState<Record<string, unknown> | null>(null);
  const [query, setQuery] = useState("");
  const [basemap, setBasemap] = useState<BasemapId>("light");
  const [counts, setCounts] = useState({ states: 0, curated: 0, sources: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void (async () => {
      try {
        const [catalogue, stateData, sourceData] = await Promise.all([
          fetchCatalogue(), fetchStates(), fetchSources(),
        ]);
        setLayers(catalogue.layers);
        setEnabled(initialLayerState(catalogue.layers));
        setStates(stateData.entities);
        setSources(sourceData.sources);
        setCounts({ states: catalogue.state_count, curated: catalogue.curated_state_count, sources: catalogue.source_count });
      } catch (err) {
        setError(err instanceof Error ? err.message : "Explorer metadata failed to load");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const visibleSources = useMemo(() => {
    if (!enabled["federal-sources"]) return sources.filter((source) => source.jurisdiction !== "federal");
    return sources;
  }, [enabled, sources]);

  async function selectState(entity: MapEntity) {
    setSelected(entity);
    setError(null);
    try {
      setStateDetail(await fetchState(entity.id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "State detail failed to load");
    }
  }

  async function runSearch(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await fetchSources(query);
      setSources(result.sources);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Source discovery failed");
    } finally {
      setLoading(false);
    }
  }

  function toggleLayer(layerId: ExplorerLayer["id"]) {
    setEnabled((current) => ({ ...current, [layerId]: !current[layerId] }));
  }

  const curatedPortal = selected?.properties.curated_portal;

  return (
    <div className="app-shell">
      <header>
        <div>
          <span className="eyebrow">FEDERAL-FIRST · SOURCE-CITED</span>
          <h1>OpenUS Public Data Explorer</h1>
          <p>Discover federal sources and selected state portals without flattening jurisdiction differences.</p>
        </div>
        <form onSubmit={runSearch} className="search-form">
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search Census, federal, Socrata, CKAN…" aria-label="Search registered sources" />
          <button type="submit">{loading ? "Searching…" : "Discover"}</button>
        </form>
      </header>

      {error ? <div className="error-banner">{error}</div> : null}

      <main>
        <aside className="sidebar" aria-label="Discovery layers">
          <div className="metric-grid">
            <div><strong>{counts.states}</strong><span>states + DC</span></div>
            <div><strong>{counts.curated}</strong><span>curated portals</span></div>
            <div><strong>{counts.sources}</strong><span>registered sources</span></div>
          </div>
          <section>
            <div className="section-title"><h2>Discovery layers</h2><span>REGISTRY</span></div>
            <DiscoveryLayers layers={layers} enabled={enabled} counts={counts} onToggle={toggleLayer} />
          </section>
          <section className="source-list">
            <div className="section-title"><h2>Source catalogue</h2><span>{visibleSources.length} SHOWN</span></div>
            {visibleSources.map((source) => (
              <a href={source.url} target="_blank" rel="noreferrer" key={`${source.name}-${source.url}`}>
                <strong>{source.name}</strong>
                <span>{source.jurisdiction} · {source.auth.replace(/_/g, " ")}</span>
                <small>{source.platform || "direct API"} · {source.status || "active"}</small>
              </a>
            ))}
            {!visibleSources.length ? <p className="empty">No registered sources match this query.</p> : null}
          </section>
        </aside>

        <section className="map-panel">
          <fieldset className="basemap-switcher">
            <legend className="sr-only">Basemap</legend>
            {(Object.entries(BASEMAPS) as Array<[BasemapId, (typeof BASEMAPS)[BasemapId]]>).map(([id, item]) => (
              <button type="button" key={id} className={basemap === id ? "active" : ""} onClick={() => setBasemap(id)}>{item.label}</button>
            ))}
          </fieldset>
          <div className="map-legend"><span className="legend-curated" /> curated portal <span className="legend-state" /> registry only</div>
          <MapContainer center={US_CENTER} zoom={4} minZoom={3} className="map" scrollWheelZoom>
            <TileLayer attribution={BASEMAPS[basemap].attribution} url={BASEMAPS[basemap].url} />
            {enabled.states && states.map((entity) => (
              <StateMarker
                key={entity.id}
                entity={entity}
                curatedLayerEnabled={Boolean(enabled["curated-portals"])}
                active={selected?.id === entity.id}
                onSelect={(item) => void selectState(item)}
              />
            ))}
            <MapFocus entity={selected} />
          </MapContainer>
        </section>

        <aside className="detail-panel">
          <div className="section-title"><h2>State discovery</h2><span>{selected ? selected.id : "SELECT"}</span></div>
          {selected ? (
            <div className="state-card">
              <div className="state-code">{selected.id}</div>
              <h3>{selected.title}</h3>
              <p>State FIPS <strong>{selected.properties.fips}</strong></p>
              <span className={`coverage ${curatedPortal ? "curated" : "registry"}`}>{curatedPortal ? "Curated portal available" : "Registry-only coverage"}</span>
              {curatedPortal ? (
                <div className="portal-card">
                  <span>OFFICIAL {curatedPortal.platform.toUpperCase()} PORTAL</span>
                  <h4>{curatedPortal.state} Open Data</h4>
                  <p>{curatedPortal.notes || "Selected state portal registered for source discovery."}</p>
                  <a href={curatedPortal.base_url} target="_blank" rel="noreferrer">Open portal ↗</a>
                </div>
              ) : (
                <div className="coverage-note">No curated portal is registered for this state yet. Generic Socrata, ArcGIS and CKAN adapters remain available where a compatible official endpoint is known.</div>
              )}
              {stateDetail ? <details className="raw"><summary>Inspect registry JSON</summary><pre>{JSON.stringify(stateDetail, null, 2)}</pre></details> : null}
            </div>
          ) : (
            <div className="empty-state"><div>⌖</div><h3>Select a state</h3><p>Inspect FIPS identity, coverage status and any curated official portal.</p></div>
          )}
          <div className="disclaimer"><strong>Discovery boundary</strong><p>Map points are approximate label centroids. They are not analytical boundaries, measurements or evidence of complete state/local coverage.</p></div>
        </aside>
      </main>
    </div>
  );
}
