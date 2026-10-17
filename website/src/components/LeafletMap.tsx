'use client';
import { useEffect, useRef } from 'react';
import type * as Leaflet from 'leaflet';

export interface MapPoint { id: string; lat: number; lng: number; label: string }
interface Props {
  points?: MapPoint[];
  activeId?: string | null;
  onSelect?: (id: string) => void;
  onMapClick?: (lat: number, lng: number) => void;
  guess?: [number, number] | null;
  answer?: [number, number] | null;
  center?: [number, number];
  zoom?: number;
  cluster?: boolean;
  basemap?: 'satellite' | 'dark';
  label: string;            // accessible name for the map region
  className?: string;
}

const TILES = {
  satellite: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Imagery © Esri, Maxar, Earthstar Geographics, and the GIS User Community',
  },
  dark: {
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
  },
};

export default function LeafletMap({ points = [], activeId, onSelect, onMapClick, guess, answer, center = [25, 0], zoom = 2,
  cluster = false, basemap = 'satellite', label, className = '' }: Props) {
  const el = useRef<HTMLDivElement>(null);
  const map = useRef<Leaflet.Map | null>(null);
  const L = useRef<typeof Leaflet | null>(null);
  const layer = useRef<Leaflet.LayerGroup | null>(null);
  const extra = useRef<Leaflet.LayerGroup | null>(null);
  const markers = useRef<Record<string, Leaflet.Marker>>({});
  const cb = useRef({ onSelect, onMapClick });
  cb.current = { onSelect, onMapClick };

  // init once
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const lf = (await import('leaflet')).default;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (window as any).L = lf;
      if (cluster) await import('leaflet.markercluster');
      if (cancelled || !el.current || map.current) return;
      L.current = lf;
      const m = lf.map(el.current, { center, zoom, minZoom: 2, worldCopyJump: true, zoomControl: true, attributionControl: true });
      lf.tileLayer(TILES[basemap].url, { attribution: TILES[basemap].attribution, maxZoom: 18 }).addTo(m);
      if (basemap === 'satellite') {
        lf.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', { maxZoom: 18, opacity: 0.85 }).addTo(m);
      }
      m.on('click', (e: Leaflet.LeafletMouseEvent) => cb.current.onMapClick?.(e.latlng.lat, e.latlng.lng));
      map.current = m;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      layer.current = cluster ? (lf as any).markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 40 }) : lf.layerGroup();
      layer.current!.addTo(m);
      extra.current = lf.layerGroup().addTo(m);
      drawPoints(); drawExtra();
    })();
    return () => { cancelled = true; map.current?.remove(); map.current = null; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const pinIcon = (cls = '') => L.current!.divIcon({ className: '', html: `<div class="mc-pin ${cls}"><span></span></div>`, iconSize: [18, 18], iconAnchor: [9, 9] });

  function drawPoints() {
    const lf = L.current; if (!lf || !layer.current) return;
    layer.current.clearLayers(); markers.current = {};
    points.forEach((p) => {
      const mk = lf.marker([p.lat, p.lng], { icon: pinIcon(p.id === activeId ? 'active' : ''), title: p.label, alt: p.label, keyboard: true, riseOnHover: true });
      mk.bindTooltip(p.label, { direction: 'top', offset: [0, -10] });
      mk.on('click', () => cb.current.onSelect?.(p.id));
      mk.on('keypress', (e: Leaflet.LeafletKeyboardEvent) => { if (e.originalEvent.key === 'Enter') cb.current.onSelect?.(p.id); });
      mk.addTo(layer.current!); markers.current[p.id] = mk;
    });
  }
  function drawExtra() {
    const lf = L.current; if (!lf || !extra.current || !map.current) return;
    extra.current.clearLayers();
    if (guess) lf.marker(guess, { icon: pinIcon('guess'), title: 'Your guess', keyboard: false }).addTo(extra.current);
    if (answer) lf.marker(answer, { icon: pinIcon('active'), title: 'Correct location', keyboard: false }).addTo(extra.current);
    if (guess && answer) {
      lf.polyline([guess, answer], { color: '#C8F34B', weight: 3, dashArray: '8 8' }).addTo(extra.current);
      map.current.flyToBounds(lf.latLngBounds([guess, answer]).pad(0.4), { duration: 0.9, maxZoom: 7 });
    }
  }

  useEffect(drawPoints, [points, activeId]);
  useEffect(drawExtra, [guess, answer]);
  useEffect(() => {
    if (!activeId || !map.current) return;
    const p = points.find((x) => x.id === activeId);
    if (p) map.current.flyTo([p.lat, p.lng], Math.max(map.current.getZoom(), 5), { duration: 0.8 });
  }, [activeId, points]);

  return <div ref={el} role="region" aria-label={label} className={`h-full w-full ${className}`} />;
}
