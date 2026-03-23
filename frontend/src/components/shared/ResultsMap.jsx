import { MapContainer, TileLayer, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const defaultCenter = [40.7128, -74.006];

const isFiniteCoord = (v) => Number.isFinite(v);

function computeCenter(points) {
  const valid = points.filter(p => isFiniteCoord(p.latitude) && isFiniteCoord(p.longitude));
  if (!valid.length) return defaultCenter;
  const avgLat = valid.reduce((sum, p) => sum + p.latitude, 0) / valid.length;
  const avgLon = valid.reduce((sum, p) => sum + p.longitude, 0) / valid.length;
  return [avgLat, avgLon];
}

export default function ResultsMap({ results, loading }) {
  const markers = (results || []).filter(r => isFiniteCoord(r.latitude) && isFiniteCoord(r.longitude));
  const hasCoords = markers.length > 0;
  const center = hasCoords ? computeCenter(markers) : defaultCenter;

  console.info('[ResultsMap] markers', markers.length, markers.slice(0, 3));

  return (
    <div className="map-card">
      <div className="map-header">
        <div>
          <div className="map-title">Map view</div>
          <div className="map-sub">Showing {loading ? '…' : markers.length} locations</div>
        </div>
      </div>
      <div className="map-frame">
        {hasCoords ? (
          <MapContainer
            key={`${center[0]}-${center[1]}-${markers.length}`}
            center={center}
            zoom={11}
            style={{ height: '460px', width: '100%' }}
            scrollWheelZoom={true}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              eventHandlers={{
                tileerror: (e) => console.error('[Tile error]', e),
                load: () => console.info('[Tile load] success'),
              }}
            />
            {markers.map(r => (
              <CircleMarker
                key={r._id}
                center={[r.latitude, r.longitude]}
                pathOptions={{ color: '#C8400A', fillColor: '#C8400A', fillOpacity: 0.8 }}
                radius={6}
              >
                <Popup>
                  <div style={{ fontWeight: 700 }}>{r.name}</div>
                  <div style={{ fontSize: '0.85rem' }}>{r.cuisine}</div>
                  <div style={{ fontSize: '0.85rem', color: '#666' }}>{r.address}</div>
                  {r.distanceMeters != null && <div style={{ fontSize: '0.8rem', color: '#888' }}>{(r.distanceMeters/1000).toFixed(2)} km</div>}
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        ) : (
          <div style={{ padding: '1rem', color: 'var(--muted)' }}>
            {loading ? 'Loading map…' : 'No coordinates available for these results.'}
          </div>
        )}
      </div>
    </div>
  );
}
