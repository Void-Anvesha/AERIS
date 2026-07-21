"use client";

import { motion, AnimatePresence } from "framer-motion";
import { X, MapPin, Thermometer, Droplets, Wind, CloudRain, TreePine, Building2, GraduationCap, Hospital, Factory, HardHat, Shield, Brain } from "lucide-react";
import type { Location } from "@/types";
import { getAqiColor, getAqiLabel } from "@/lib/utils";

interface DetailsDrawerProps {
  location: Location | null;
  open: boolean;
  onClose: () => void;
}

export default function DetailsDrawer({ location, open, onClose }: DetailsDrawerProps) {
  if (!location) return null;

  const aqiColor = getAqiColor(location.currentAqi);

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
            onClick={onClose}
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 28, stiffness: 220 }}
            className="fixed right-0 top-0 h-screen z-50 overflow-y-auto w-full max-w-[420px] p-6 flex flex-col"
            style={{
              background: "rgba(24, 24, 27, 0.85)",
              backdropFilter: "blur(24px)",
              borderLeft: "1px solid rgba(255, 255, 255, 0.05)",
            }}
          >
            {/* Header */}
            <div className="flex items-start justify-between border-b border-white/[0.04] pb-5 flex-shrink-0">
              <div>
                <h2 className="text-lg font-bold text-zinc-100">{location.city}</h2>
                <p className="text-xs text-zinc-500 mt-0.5">{location.ward ? `${location.ward}, ` : ""}{location.state}</p>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-center px-3 py-1.5 rounded-xl" style={{ background: `${aqiColor}08` }}>
                  <span className="text-xl font-bold" style={{ color: aqiColor }}>{location.currentAqi}</span>
                  <p className="font-bold text-[8px] uppercase tracking-wider mt-0.5" style={{ color: aqiColor }}>{getAqiLabel(location.currentAqi)}</p>
                </div>
                <button onClick={onClose} className="p-1.5 rounded-xl hover:bg-white/5 text-zinc-400 hover:text-white transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Content list */}
            <div className="flex-1 space-y-6 pt-5">
              {/* Coordinates */}
              <Section title="Coordinates">
                <InfoRow icon={<MapPin className="w-3.5 h-3.5" />} label="Latitude" value={`${location.latitude.toFixed(4)}°N`} />
                <InfoRow icon={<MapPin className="w-3.5 h-3.5" />} label="Longitude" value={`${location.longitude.toFixed(4)}°E`} />
              </Section>

              {/* Weather */}
              <Section title="Weather Conditions">
                <div className="grid grid-cols-2 gap-2">
                  <MetricCard icon={<Thermometer className="w-3.5 h-3.5" />} label="Temperature" value={`${location.temperature}°C`} color="#F59E0B" />
                  <MetricCard icon={<Droplets className="w-3.5 h-3.5" />} label="Humidity" value={`${location.humidity}%`} color="#3B82F6" />
                  <MetricCard icon={<Wind className="w-3.5 h-3.5" />} label="Wind Speed" value={`${location.windSpeed} km/h`} color="#22C55E" />
                  <MetricCard icon={<CloudRain className="w-3.5 h-3.5" />} label="Rainfall" value={`${location.rainfall} mm`} color="#6366F1" />
                </div>
              </Section>

              {/* Pollutants */}
              <Section title="Pollutant Levels">
                <div className="grid grid-cols-2 gap-2">
                  <PollutantBar label="PM2.5" value={location.pollutants.pm25} max={300} color="#EF4444" />
                  <PollutantBar label="PM10" value={location.pollutants.pm10} max={400} color="#F59E0B" />
                  <PollutantBar label="NO₂" value={location.pollutants.no2} max={100} color="#3B82F6" />
                  <PollutantBar label="CO" value={location.pollutants.co} max={10} color="#A855F7" />
                  <PollutantBar label="SO₂" value={location.pollutants.so2} max={50} color="#3B82F6" />
                  <PollutantBar label="O₃" value={location.pollutants.o3} max={100} color="#22C55E" />
                </div>
              </Section>

              {/* Nearby Infrastructure */}
              <Section title="Nearby Infrastructure">
                <div className="grid grid-cols-2 gap-2">
                  <MetricCard icon={<Building2 className="w-3.5 h-3.5" />} label="Roads" value={`${location.nearbyRoads}`} color="#A1A1AA" />
                  <MetricCard icon={<GraduationCap className="w-3.5 h-3.5" />} label="Schools" value={`${location.nearbySchools}`} color="#F59E0B" />
                  <MetricCard icon={<Hospital className="w-3.5 h-3.5" />} label="Hospitals" value={`${location.nearbyHospitals}`} color="#EF4444" />
                  <MetricCard icon={<Factory className="w-3.5 h-3.5" />} label="Industries" value={`${location.nearbyIndustries}`} color="#A855F7" />
                  <MetricCard icon={<HardHat className="w-3.5 h-3.5" />} label="Construction" value={`${location.nearbyConstructionSites}`} color="#F59E0B" />
                  <MetricCard icon={<TreePine className="w-3.5 h-3.5" />} label="Green Cover" value={`${location.greenCoverPercent}%`} color="#22C55E" />
                </div>
              </Section>

              {/* Risk Assessment */}
              <Section title="Risk Assessment">
                <InfoRow icon={<Shield className="w-3.5 h-3.5" />} label="Health Risk" value={location.healthRisk} valueColor={location.healthRisk === "Severe" ? "#EF4444" : location.healthRisk === "Very High" ? "#F59E0B" : location.healthRisk === "High" ? "#F59E0B" : "#22C55E"} />
                <InfoRow icon={<Shield className="w-3.5 h-3.5" />} label="Priority" value={location.priorityLevel} valueColor="#3B82F6" />
                <InfoRow icon={<Shield className="w-3.5 h-3.5" />} label="Confidence" value={`${location.confidenceScore}%`} valueColor="#22C55E" />
              </Section>

              {/* AI Recommendation */}
              <Section title="AI Recommendation">
                <div className="flex items-start gap-3 p-3.5 rounded-xl border border-blue-500/10 bg-blue-500/5">
                  <Brain className="w-4 h-4 flex-shrink-0 mt-0.5 text-blue-400" />
                  <p className="text-xs text-zinc-300 leading-relaxed font-serif">{location.recommendation}</p>
                </div>
              </Section>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// Sub-components

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <h4 className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">{title}</h4>
      {children}
    </div>
  );
}

function InfoRow({ icon, label, value, valueColor }: { icon: React.ReactNode; label: string; value: string; valueColor?: string }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-white/[0.02] last:border-0">
      <div className="flex items-center gap-2 text-zinc-400">
        <span className="text-zinc-500">{icon}</span>
        <span className="text-xs">{label}</span>
      </div>
      <span className="text-xs font-semibold" style={{ color: valueColor || "#FAFAFA" }}>{value}</span>
    </div>
  );
}

function MetricCard({ icon, label, value, color }: { icon: React.ReactNode; label: string; value: string; color: string }) {
  return (
    <div className="p-3 rounded-xl border border-white/5 bg-zinc-900/30">
      <div className="flex items-center gap-1.5 mb-1">
        <span style={{ color, scale: 0.85 }}>{icon}</span>
        <span className="text-zinc-500 text-[10px] font-medium">{label}</span>
      </div>
      <span className="text-xs font-bold text-zinc-200">{value}</span>
    </div>
  );
}

function PollutantBar({ label, value, max, color }: { label: string; value: number; max: number; color: string }) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div className="p-3 rounded-xl border border-white/5 bg-zinc-900/30">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-[10px] font-medium text-zinc-400">{label}</span>
        <span className="text-[10px] font-bold" style={{ color }}>{value}</span>
      </div>
      <div className="h-1 rounded-full overflow-hidden bg-zinc-800">
        <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 0.8, ease: "easeOut" }} className="h-full rounded-full" style={{ background: color }} />
      </div>
    </div>
  );
}
