"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import dynamicComponent from "next/dynamic";
import {
  Activity,
  BarChart3,
  AlertTriangle,
  Bell,
  MapPin,
  Radio,
  Map as MapIcon,
  Sparkles,
  ArrowRight,
  ShieldAlert,
  Flame,
  Zap,
} from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";
import { useDashboard, useLocations } from "@/hooks/useApi";
import KpiCard from "@/components/dashboard/KpiCard";
import AlertsFeed from "@/components/dashboard/AlertsFeed";
import PageHeader from "@/components/shared/PageHeader";
import LoadingSkeleton from "@/components/shared/LoadingSkeleton";
import ErrorState from "@/components/shared/ErrorState";
import { getAqiColor } from "@/lib/utils";
import DetailsDrawer from "@/components/map/DetailsDrawer";

const AqiTrendChart = dynamicComponent(() => import("@/components/charts/AqiTrendChart"), { ssr: false });
import type { Location, MapLayer } from "@/types";

// Dynamic import for Leaflet map on dashboard
const AqiMap = dynamicComponent(() => import("@/components/map/AqiMap"), { ssr: false });

export default function DashboardPage() {
  const { data, isLoading, error, refetch } = useDashboard();
  const { data: locations } = useLocations();

  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activeLayer, setActiveLayer] = useState<MapLayer>("markers");

  const handleMarkerClick = (loc: Location) => {
    setSelectedLocation(loc);
    setDrawerOpen(true);
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <LoadingSkeleton count={6} />
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8 space-y-4">
            <LoadingSkeleton variant="chart" />
          </div>
          <div className="lg:col-span-4">
            <LoadingSkeleton count={4} />
          </div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div>
        <ErrorState onRetry={() => refetch()} />
      </div>
    );
  }

  const worstCityColor = getAqiColor(data.worstCityAqi);

  return (
    <div className="space-y-6 cyber-grid min-h-screen">
      {/* Top Header with Telemetry Status Beacons */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-white/[0.04]">
        <PageHeader
          title="Command Center"
          subtitle="Real-time Urban Air Quality Intelligence & Autonomous Protocol Mesh"
          icon={<Activity className="w-5 h-5" style={{ color: "#3B82F6" }} />}
        />

        {/* Live Beacons & Actions */}
        <div className="flex flex-wrap items-center gap-2.5">
          <div
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-500/10 border border-blue-500/20 text-blue-400"
          >
            <Zap className="w-3.5 h-3.5 animate-pulse" />
            <span>AI CORE LIVE</span>
          </div>

          <Link href="/map">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-md"
              style={{
                background: "linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)",
                color: "#FAFAFA",
                boxShadow: "0 4px 12px rgba(59, 130, 246, 0.25)",
              }}
            >
              <MapIcon className="w-3.5 h-3.5" />
              <span>Full GIS Studio</span>
            </motion.button>
          </Link>

          <Link href="/assistant">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all"
              style={{
                background: "rgba(255, 255, 255, 0.02)",
                color: "#FAFAFA",
                border: "1px solid rgba(255, 255, 255, 0.05)",
              }}
            >
              <Sparkles className="w-3.5 h-3.5 text-blue-400" />
              <span>Ask AERIS AI</span>
            </motion.button>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-6 gap-4">
        <KpiCard
          title="Current AQI"
          value={data.currentAqi}
          trend={data.trends.currentAqiTrend}
          icon={<Activity className="w-4 h-4" />}
          color={getAqiColor(data.currentAqi)}
          sparkline={data.sparklines.currentAqi}
          subtitle="National Index"
          delay={0}
        />
        <KpiCard
          title="Average AQI"
          value={data.averageAqi}
          trend={data.trends.averageAqiTrend}
          icon={<BarChart3 className="w-4 h-4" />}
          color="#F59E0B"
          sparkline={data.sparklines.averageAqi}
          subtitle="24h Rolling Mean"
          delay={1}
        />
        <KpiCard
          title="High Risk"
          value={data.highRiskAreas}
          trend={data.trends.highRiskTrend}
          icon={<AlertTriangle className="w-4 h-4" />}
          color="#EF4444"
          sparkline={data.sparklines.highRisk}
          subtitle="Areas AQI > 200"
          delay={2}
        />
        <KpiCard
          title="Active Alerts"
          value={data.activeAlerts}
          trend={data.trends.alertsTrend}
          icon={<Bell className="w-4 h-4" />}
          color="#A855F7"
          sparkline={data.sparklines.alerts}
          subtitle="Sensor Anomalies"
          delay={3}
        />
        <KpiCard
          title="Worst City"
          value={data.worstCityAqi}
          icon={<MapPin className="w-4 h-4" />}
          color={worstCityColor}
          subtitle={data.worstCity}
          delay={4}
        />
        <KpiCard
          title="Stations"
          value={data.monitoringStations}
          icon={<Radio className="w-4 h-4" />}
          color="#22C55E"
          subtitle="Active IoT Mesh"
          delay={5}
        />
      </div>

      {/* Main Command Center Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (8 cols on lg) */}
        <div className="lg:col-span-8 space-y-6">
          {/* Live GIS Map Widget on Dashboard */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="rounded-2xl overflow-hidden relative flex flex-col"
            style={{
              height: 440,
              background: "rgba(24, 24, 27, 0.6)",
              backdropFilter: "blur(16px)",
              border: "1px solid rgba(255, 255, 255, 0.04)",
              boxShadow: "0 10px 30px rgba(0, 0, 0, 0.5)",
            }}
          >
            {/* Map Widget Header */}
            <div className="px-5 py-3.5 z-20 flex items-center justify-between border-b border-white/[0.04]" style={{ background: "rgba(24, 24, 27, 0.9)" }}>
              <div className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full animate-ping bg-blue-500" />
                <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">
                  Live Environmental GIS Mesh
                </h3>
                <span className="text-[9px] text-zinc-500 font-mono hidden sm:inline">
                  ({locations?.length || 0} Nodes Connected)
                </span>
              </div>

              {/* Layer Controls */}
              <div className="flex items-center gap-1">
                {(["markers", "heatmap", "satellite"] as MapLayer[]).map((layer) => (
                  <button
                    key={layer}
                    onClick={() => setActiveLayer(layer)}
                    className="px-2.5 py-1 rounded-lg text-[10px] font-bold capitalize transition-all"
                    style={{
                      background: activeLayer === layer ? "rgba(59, 130, 246, 0.1)" : "rgba(255, 255, 255, 0.02)",
                      color: activeLayer === layer ? "#3B82F6" : "#A1A1AA",
                      border: `1px solid ${activeLayer === layer ? "rgba(59, 130, 246, 0.25)" : "rgba(255, 255, 255, 0.04)"}`,
                    }}
                  >
                    {layer}
                  </button>
                ))}
              </div>
            </div>

            {/* Map Canvas */}
            <div className="flex-1 relative">
              <AqiMap
                locations={locations || []}
                onMarkerClick={handleMarkerClick}
                activeLayer={activeLayer}
              />
            </div>
          </motion.div>

          {/* National Telemetry & Pollutants Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* National AQI Telemetry Chart */}
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="rounded-2xl p-5 space-y-3"
              style={{
                background: "rgba(24, 24, 27, 0.6)",
                backdropFilter: "blur(16px)",
                border: "1px solid rgba(255, 255, 255, 0.04)",
              }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">
                    24h National Telemetry
                  </h3>
                  <p className="text-[10px] text-zinc-500 font-medium">CPCB Monitoring Stream</p>
                </div>
                <Link href="/forecast">
                  <span className="text-[11px] text-blue-400 hover:text-blue-300 font-bold flex items-center gap-1 cursor-pointer transition-colors">
                    Analytics <ArrowRight className="w-3 h-3" />
                  </span>
                </Link>
              </div>

              <div className="pt-1">
                <AqiTrendChart
                  data={[
                    { time: "00:00", aqi: 165, pm25: 88, pm10: 140 },
                    { time: "04:00", aqi: 152, pm25: 78, pm10: 130 },
                    { time: "08:00", aqi: 189, pm25: 110, pm10: 175 },
                    { time: "12:00", aqi: 198, pm25: 125, pm10: 190 },
                    { time: "16:00", aqi: 175, pm25: 98, pm10: 155 },
                    { time: "20:00", aqi: 187, pm25: 115, pm10: 168 },
                    { time: "24:00", aqi: 192, pm25: 120, pm10: 172 },
                  ]}
                />
              </div>
            </motion.div>

            {/* Pollutant Level Progress Bars */}
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.25 }}
              className="rounded-2xl p-5 space-y-4"
              style={{
                background: "rgba(24, 24, 27, 0.6)",
                backdropFilter: "blur(16px)",
                border: "1px solid rgba(255, 255, 255, 0.04)",
              }}
            >
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">
                  National Pollutant Thresholds
                </h3>
                <span className="text-[9px] text-zinc-500 font-mono font-bold">NAQI METRIC</span>
              </div>

              <div className="space-y-3 pt-1">
                {[
                  { name: "PM2.5 (Fine Particulate)", val: 115, max: 250, unit: "µg/m³", color: "#EF4444", status: "Severe" },
                  { name: "PM10 (Coarse Dust)", val: 168, max: 350, unit: "µg/m³", color: "#F59E0B", status: "Poor" },
                  { name: "NO₂ (Nitrogen Dioxide)", val: 64, max: 120, unit: "ppb", color: "#3B82F6", status: "Moderate" },
                  { name: "O₃ (Ozone)", val: 42, max: 100, unit: "ppb", color: "#22C55E", status: "Good" },
                ].map((p, i) => {
                  const pct = Math.min(100, (p.val / p.max) * 100);
                  return (
                    <div key={i} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-zinc-300 font-semibold text-[11px]">{p.name}</span>
                        <div className="flex items-center gap-1.5">
                          <span className="font-bold text-zinc-100 text-[11px]">{p.val} <span className="text-[9px] text-zinc-500 font-normal">{p.unit}</span></span>
                          <span className="text-[8px] font-bold px-1.5 py-0.2 rounded" style={{ background: `${p.color}08`, color: p.color }}>{p.status}</span>
                        </div>
                      </div>
                      <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255, 255, 255, 0.03)" }}>
                        <div
                          className="h-full rounded-full transition-all duration-500"
                          style={{ width: `${pct}%`, background: p.color }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Right Column (4 cols on lg) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Live Alert Feed */}
          <div className="h-[440px]">
            <AlertsFeed alerts={data.recentAlerts} />
          </div>

          {/* Top Critical Hotspot Cities */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            className="rounded-2xl p-5 space-y-3"
            style={{
              background: "rgba(24, 24, 27, 0.6)",
              backdropFilter: "blur(16px)",
              border: "1px solid rgba(255, 255, 255, 0.04)",
            }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Flame className="w-4 h-4 text-red-500" />
                <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">Top Critical Hotspots</h3>
              </div>
              <Link href="/hotspots">
                <span className="text-[11px] text-blue-400 font-bold cursor-pointer hover:underline">View All 10</span>
              </Link>
            </div>

            <div className="space-y-2">
              {[
                { city: "Ghaziabad", state: "Uttar Pradesh", aqi: 335, risk: "Severe", color: "#A855F7" },
                { city: "Delhi", state: "NCR", aqi: 312, risk: "Severe", color: "#EF4444" },
                { city: "Kanpur", state: "Uttar Pradesh", aqi: 278, risk: "Very High", color: "#F59E0B" },
                { city: "Lucknow", state: "Uttar Pradesh", aqi: 245, risk: "High", color: "#3B82F6" },
              ].map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2.5 rounded-xl transition-colors hover:bg-white/[0.02]"
                  style={{ background: "rgba(255, 255, 255, 0.01)", border: "1px solid rgba(255, 255, 255, 0.03)" }}
                >
                  <div className="flex items-center gap-2.5">
                    <span className="w-5.5 h-5.5 rounded-lg text-[10px] font-bold flex items-center justify-center" style={{ background: `${item.color}10`, color: item.color }}>
                      {idx + 1}
                    </span>
                    <div>
                      <p className="text-xs font-bold text-zinc-200 leading-tight">{item.city}</p>
                      <p className="text-[9px] text-zinc-500 leading-tight">{item.state}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-extrabold" style={{ color: item.color }}>{item.aqi}</span>
                    <p className="text-[8px] font-bold uppercase tracking-wider" style={{ color: item.color }}>{item.risk}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* AI Autonomous Advisory Widget */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="rounded-2xl p-5 space-y-3.5 relative overflow-hidden"
            style={{
              background: "linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(24, 24, 27, 0.8) 100%)",
              backdropFilter: "blur(16px)",
              border: "1px solid rgba(59, 130, 246, 0.2)",
              boxShadow: "0 0 25px rgba(59, 130, 246, 0.05)",
            }}
          >
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl" style={{ background: "rgba(59, 130, 246, 0.1)", color: "#3B82F6" }}>
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">AERIS AI Protocol</h3>
                <p className="text-[10px] text-blue-400 font-medium">Smart City Autonomous Directives</p>
              </div>
            </div>

            <div className="p-3.5 rounded-xl bg-zinc-950/80 border border-white/[0.04] space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-red-400 flex items-center gap-1 text-[11px]">
                  <ShieldAlert className="w-3.5 h-3.5" /> Stage-IV Directive
                </span>
                <span className="text-[8px] text-zinc-500 font-mono font-bold">AUTONOMOUS</span>
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                Deploy anti-smog water cannons along NH-24 corridor. Ghaziabad PM2.5 levels exceeding safe threshold by 340%.
              </p>
            </div>

            <Link href="/assistant">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full py-2.5 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5"
                style={{
                  background: "rgba(59, 130, 246, 0.12)",
                  color: "#3B82F6",
                  border: "1px solid rgba(59, 130, 246, 0.25)",
                }}
              >
                <span>Consult AI Assistant</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </motion.button>
            </Link>
          </motion.div>
        </div>
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
