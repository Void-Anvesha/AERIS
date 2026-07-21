"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import dynamicComponent from "next/dynamic";
import { Map } from "lucide-react";
import { useLocations } from "@/hooks/useApi";
import PageHeader from "@/components/shared/PageHeader";
import LoadingSkeleton from "@/components/shared/LoadingSkeleton";
import ErrorState from "@/components/shared/ErrorState";
import DetailsDrawer from "@/components/map/DetailsDrawer";
import FilterPanel from "@/components/map/FilterPanel";
import TimelineSlider from "@/components/map/TimelineSlider";
import type { Location, MapLayer, TimelinePosition, FilterState } from "@/types";

// Dynamic import to avoid SSR issues with Leaflet
const AqiMap = dynamicComponent(() => import("@/components/map/AqiMap"), { ssr: false });

const defaultFilters: FilterState = {
  state: "",
  city: "",
  aqiMin: 0,
  aqiMax: 500,
  pollutant: "",
  date: "",
  season: "",
  priority: "",
  searchCoords: "",
  searchCity: "",
};

export default function MapPage() {
  const { data: locations, isLoading, error, refetch } = useLocations();
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activeLayer, setActiveLayer] = useState<MapLayer>("markers");
  const [timeline, setTimeline] = useState<TimelinePosition>("today");
  const [filters, setFilters] = useState<FilterState>(defaultFilters);
  const [showFilters, setShowFilters] = useState(false);

  const handleMarkerClick = (location: Location) => {
    setSelectedLocation(location);
    setDrawerOpen(true);
  };

  // Apply filters
  const filteredLocations = locations?.filter((loc) => {
    if (filters.state && loc.state !== filters.state) return false;
    if (filters.city && !loc.city.toLowerCase().includes(filters.city.toLowerCase())) return false;
    if (loc.currentAqi < filters.aqiMin || loc.currentAqi > filters.aqiMax) return false;
    if (filters.priority && loc.priorityLevel !== filters.priority) return false;
    if (filters.searchCity && !loc.city.toLowerCase().includes(filters.searchCity.toLowerCase()))
      return false;
    return true;
  });

  if (isLoading) {
    return (
      <div className="p-6">
        <LoadingSkeleton variant="chart" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <ErrorState onRetry={() => refetch()} />
      </div>
    );
  }

  return (
    <div className="flex-1 relative flex flex-col min-h-[calc(100vh-10rem)] w-full rounded-2xl overflow-hidden border border-white/5 shadow-2xl">
      {/* Map - Occupies most/all screen space in this panel */}
      <div className="absolute inset-0 z-0">
        <AqiMap
          locations={filteredLocations || []}
          onMarkerClick={handleMarkerClick}
          activeLayer={activeLayer}
        />
      </div>

      {/* Floating Top Controls Panel */}
      <div className="absolute top-4 left-4 right-4 z-10 flex flex-col gap-3 pointer-events-none">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 w-full">
          {/* Header Card */}
          <div
            className="p-3.5 rounded-2xl shadow-xl flex items-center gap-3 backdrop-blur-md pointer-events-auto border border-white/5"
            style={{ background: "rgba(24, 24, 27, 0.85)" }}
          >
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center">
              <Map className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-xs font-bold text-zinc-100 uppercase tracking-wider leading-none">AQI GIS Studio</h2>
              <p className="text-[9px] text-zinc-500 mt-1 font-medium leading-none">Monitoring {filteredLocations?.length || 0} Stations</p>
            </div>
          </div>

          {/* Controller Row */}
          <div className="flex flex-wrap items-center gap-2 pointer-events-auto">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all shadow-md border"
              style={{
                background: showFilters ? "rgba(59, 130, 246, 0.15)" : "rgba(24, 24, 27, 0.8)",
                color: showFilters ? "#3B82F6" : "#A1A1AA",
                borderColor: showFilters ? "rgba(59, 130, 246, 0.3)" : "rgba(255, 255, 255, 0.05)",
                backdropFilter: "blur(12px)",
              }}
            >
              Filters
            </button>

            <div className="flex p-0.5 rounded-xl border border-white/5 shadow-md bg-zinc-900/80" style={{ backdropFilter: "blur(12px)" }}>
              {(["markers", "heatmap", "satellite"] as MapLayer[]).map((layer) => (
                <button
                  key={layer}
                  onClick={() => setActiveLayer(layer)}
                  className={`px-3 py-1.5 rounded-lg text-[9px] font-bold capitalize transition-all ${
                    activeLayer === layer ? "text-blue-400 bg-blue-500/10" : "text-zinc-400 hover:text-zinc-200"
                  }`}
                >
                  {layer}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Floating Filter Panel Overlay */}
        {showFilters && (
          <div className="max-w-4xl w-full pointer-events-auto">
            <FilterPanel
              filters={filters}
              onChange={setFilters}
              onReset={() => setFilters(defaultFilters)}
            />
          </div>
        )}
      </div>

      {/* Floating Bottom Timeline overlay */}
      <div className="absolute bottom-6 left-6 right-6 z-10 max-w-2xl mx-auto w-full pointer-events-auto">
        <TimelineSlider value={timeline} onChange={setTimeline} />
      </div>

      {/* Details Drawer */}
      <DetailsDrawer
        location={selectedLocation}
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      />
    </div>
  );
}
