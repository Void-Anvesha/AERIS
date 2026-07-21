"use client";

export const dynamic = "force-dynamic";

import { motion } from "framer-motion";
import { Flame, ExternalLink } from "lucide-react";
import Link from "next/link";
import { useHotspots } from "@/hooks/useApi";
import PageHeader from "@/components/shared/PageHeader";
import LoadingSkeleton from "@/components/shared/LoadingSkeleton";
import { getAqiColor } from "@/lib/utils";

export default function HotspotsPage() {
  const { data: hotspots, isLoading } = useHotspots();

  if (isLoading) {
    return (
      <div className="space-y-4">
        <LoadingSkeleton count={10} variant="line" />
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      <div className="pb-4 border-b border-white/[0.04]">
        <PageHeader
          title="Hotspot Logs"
          subtitle="Top 10 High Risk Locations requiring sensor inspections and mitigation workflows"
          icon={<Flame className="w-5 h-5" style={{ color: "#EF4444" }} />}
        />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl overflow-hidden border border-white/5 shadow-lg"
        style={{
          background: "rgba(24, 24, 27, 0.6)",
          backdropFilter: "blur(16px)",
        }}
      >
        {/* Table Header */}
        <div
          className="grid gap-2 px-5 py-3 font-bold text-zinc-500 uppercase tracking-widest border-b border-white/[0.04]"
          style={{ gridTemplateColumns: "60px 1.2fr 1.2fr 80px 80px 100px 1.5fr 1.5fr 80px", fontSize: 9 }}
        >
          <span>Rank</span>
          <span>Location</span>
          <span>Coordinates</span>
          <span>AQI</span>
          <span>Forecast</span>
          <span>Risk</span>
          <span>Reason</span>
          <span>Action</span>
          <span className="text-right">Map</span>
        </div>

        {/* Table Rows */}
        {hotspots?.map((hotspot, i) => {
          const riskColors: Record<string, string> = {
            Severe: "#EF4444",
            "Very High": "#F59E0B",
            High: "#3B82F6",
          };
          const riskColor = riskColors[hotspot.risk] || "#F59E0B";

          return (
            <motion.div
              key={hotspot.rank}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.04 }}
              className="grid gap-2 px-5 py-4 items-center cursor-pointer transition-colors hover:bg-white/[0.02]"
              style={{ gridTemplateColumns: "60px 1.2fr 1.2fr 80px 80px 100px 1.5fr 1.5fr 80px", borderBottom: "1px solid rgba(255,255,255,0.02)" }}
            >
              {/* Rank */}
              <span
                className="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold"
                style={{
                  background: i < 3 ? `${riskColor}08` : "rgba(255,255,255,0.02)",
                  color: i < 3 ? riskColor : "#71717A",
                }}
              >
                {hotspot.rank}
              </span>

              {/* Location */}
              <div>
                <p className="text-xs font-bold text-zinc-200">{hotspot.city}</p>
                <p className="text-[10px] text-zinc-500 mt-0.5">{hotspot.state}</p>
              </div>

              {/* Coordinates */}
              <span className="text-[10px] text-zinc-500 font-mono">
                {hotspot.latitude.toFixed(4)}, {hotspot.longitude.toFixed(4)}
              </span>

              {/* AQI */}
              <span
                className="text-xs font-bold"
                style={{ color: getAqiColor(hotspot.aqi) }}
              >
                {hotspot.aqi}
              </span>

              {/* Forecast */}
              <span
                className="text-xs font-bold text-zinc-400"
                style={{ color: getAqiColor(hotspot.forecastAqi) }}
              >
                {hotspot.forecastAqi}
              </span>

              {/* Risk */}
              <span
                className="text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wide w-fit"
                style={{
                  background: `${riskColor}08`,
                  color: riskColor,
                }}
              >
                {hotspot.risk}
              </span>

              {/* Reason */}
              <span className="text-[11px] text-zinc-400 leading-normal">{hotspot.reason}</span>

              {/* Action */}
              <span className="text-[11px] text-zinc-400 leading-normal">{hotspot.action}</span>

              {/* Map Link */}
              <div className="flex justify-end">
                <Link href="/map">
                  <span
                    className="flex items-center gap-1 text-[10px] font-bold px-2 py-1.5 rounded-lg transition-colors hover:bg-blue-500/10 text-blue-400 bg-blue-500/5 border border-blue-500/10"
                  >
                    <ExternalLink className="w-3 h-3" />
                    View
                  </span>
                </Link>
              </div>
            </motion.div>
          );
        })}
      </motion.div>
    </div>
  );
}
