"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import type { Location, MapLayer } from "@/types";
import { getAqiColor, getAqiLabel } from "@/lib/utils";
import MarkerPopup from "./MarkerPopup";

// Fix Leaflet default icon issue
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function createAqiIcon(aqi: number) {
  const color = getAqiColor(aqi);
  return L.divIcon({
    className: "custom-aqi-marker",
    html: `
      <div style="
        width: 36px; height: 36px;
        border-radius: 50%;
        background: ${color};
        border: 3px solid rgba(255,255,255,0.3);
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 700; color: #fff;
        box-shadow: 0 2px 8px ${color}80, 0 0 20px ${color}30;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        position: relative;
      ">
        ${aqi}
        <div style="
          position: absolute; inset: -4px;
          border-radius: 50%;
          border: 2px solid ${color}40;
          animation: pulse-ring 2s ease-out infinite;
        "></div>
      </div>
    `,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -20],
  });
}

// Tile layer configs
const tileLayers: Record<MapLayer, { url: string; attribution: string }> = {
  markers: {
    url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
  },
  heatmap: {
    url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
  },
  satellite: {
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution: "&copy; Esri",
  },
  terrain: {
    url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
  },
};

// Heatmap overlay component
function HeatmapLayer({ locations }: { locations: Location[] }) {
  const map = useMap();

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-require-imports, @typescript-eslint/no-explicit-any
    const heat = require("leaflet.heat");
    void heat;

    const points = locations.map((loc) => [
      loc.latitude,
      loc.longitude,
      loc.currentAqi / 500,
    ] as [number, number, number]);

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const LHeat = L as any;
    const heatLayer = LHeat.heatLayer
      ? LHeat.heatLayer(points, {
          radius: 35,
          blur: 25,
          maxZoom: 10,
          gradient: {
            0.0: "#22C55E",
            0.25: "#F59E0B",
            0.5: "#F97316",
            0.75: "#EF4444",
            1.0: "#A855F7",
          },
        })
      : null;

    if (heatLayer) {
      heatLayer.addTo(map);
      return () => {
        map.removeLayer(heatLayer);
      };
    }
  }, [locations, map]);

  return null;
}

interface AqiMapProps {
  locations: Location[];
  onMarkerClick: (location: Location) => void;
  activeLayer: MapLayer;
}

export default function AqiMap({ locations, onMarkerClick, activeLayer }: AqiMapProps) {
  const tileConfig = tileLayers[activeLayer];
  const showHeatmap = activeLayer === "heatmap";

  return (
    <MapContainer
      center={[22.5, 78.9]}
      zoom={5}
      className="w-full h-full"
      zoomControl={true}
      style={{ background: "#0F172A" }}
    >
      <TileLayer url={tileConfig.url} attribution={tileConfig.attribution} />

      {showHeatmap && <HeatmapLayer locations={locations} />}

      {!showHeatmap &&
        locations.map((loc) => (
          <Marker
            key={loc.id}
            position={[loc.latitude, loc.longitude]}
            icon={createAqiIcon(loc.currentAqi)}
            eventHandlers={{
              click: () => onMarkerClick(loc),
            }}
          >
            <Popup maxWidth={320} minWidth={280}>
              <MarkerPopup location={loc} />
            </Popup>
          </Marker>
        ))}
    </MapContainer>
  );
}
