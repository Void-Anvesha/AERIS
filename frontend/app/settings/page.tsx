"use client";

export const dynamic = "force-dynamic";

import { motion } from "framer-motion";
import { Settings as SettingsIcon, Monitor, Bell, RefreshCw, Palette } from "lucide-react";
import PageHeader from "@/components/shared/PageHeader";

const settingsSections = [
  {
    title: "Appearance",
    icon: <Palette className="w-4 h-4" />,
    color: "#A855F7",
    items: [
      { label: "Theme", value: "Dark Mode", type: "toggle", enabled: true },
      { label: "Map Style", value: "CARTO Dark", type: "select" },
      { label: "Animations", value: "Enabled", type: "toggle", enabled: true },
      { label: "Compact Mode", value: "Disabled", type: "toggle", enabled: false },
    ],
  },
  {
    title: "Notifications",
    icon: <Bell className="w-4 h-4" />,
    color: "#F59E0B",
    items: [
      { label: "Critical Alerts", value: "AQI > 300", type: "toggle", enabled: true },
      { label: "Daily Summary", value: "8:00 AM", type: "toggle", enabled: true },
      { label: "Forecast Alerts", value: "Enabled", type: "toggle", enabled: true },
      { label: "Sound", value: "Disabled", type: "toggle", enabled: false },
    ],
  },
  {
    title: "Data & Refresh",
    icon: <RefreshCw className="w-4 h-4" />,
    color: "#22C55E",
    items: [
      { label: "Auto Refresh", value: "Every 30 seconds", type: "select" },
      { label: "Data Quality", value: "High Confidence Only", type: "select" },
      { label: "Historical Data", value: "Last 30 days", type: "select" },
      { label: "Cache", value: "Enabled", type: "toggle", enabled: true },
    ],
  },
  {
    title: "Display",
    icon: <Monitor className="w-4 h-4" />,
    color: "#3B82F6",
    items: [
      { label: "AQI Standard", value: "India (NAQI)", type: "select" },
      { label: "Temperature Unit", value: "Celsius (°C)", type: "select" },
      { label: "Wind Speed Unit", value: "km/h", type: "select" },
      { label: "Date Format", value: "DD/MM/YYYY", type: "select" },
    ],
  },
];

export default function SettingsPage() {
  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      <div className="pb-4 border-b border-white/[0.04]">
        <PageHeader
          title="Settings"
          subtitle="Configure your AERIS dashboard parameters, notifications, and telemetry constraints"
          icon={<SettingsIcon className="w-5 h-5" style={{ color: "#3B82F6" }} />}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {settingsSections.map((section, si) => (
          <motion.div
            key={section.title}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: si * 0.08 }}
            className="rounded-2xl overflow-hidden border border-white/5"
            style={{
              background: "rgba(24, 24, 27, 0.6)",
              backdropFilter: "blur(16px)",
            }}
          >
            {/* Section Header */}
            <div className="px-5 py-4 border-b border-white/[0.04] flex items-center gap-3">
              <span style={{ color: section.color }}>{section.icon}</span>
              <h3 className="text-xs font-bold uppercase tracking-wider text-zinc-200">{section.title}</h3>
            </div>

            {/* Items */}
            <div className="divide-y divide-white/[0.02]">
              {section.items.map((item) => (
                <div key={item.label} className="flex items-center justify-between px-5 py-3.5">
                  <span className="text-xs text-zinc-300 font-medium">{item.label}</span>
                  {item.type === "toggle" ? (
                    <div
                      className="w-9 h-5 rounded-full relative cursor-pointer transition-colors"
                      style={{
                        background: item.enabled
                          ? "rgba(59, 130, 246, 0.2)"
                          : "rgba(255, 255, 255, 0.05)",
                        border: `1px solid ${item.enabled ? "rgba(59, 130, 246, 0.3)" : "rgba(255, 255, 255, 0.05)"}`,
                      }}
                    >
                      <div
                        className="w-3.5 h-3.5 rounded-full absolute top-0.5 transition-all"
                        style={{
                          background: item.enabled ? "#3B82F6" : "#52525B",
                          left: item.enabled ? 18 : 2,
                        }}
                      />
                    </div>
                  ) : (
                    <span className="text-[10px] font-bold text-zinc-400 px-2.5 py-1 rounded-lg border border-white/5 bg-zinc-950/30">
                      {item.value}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
