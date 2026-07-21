"use client";

import { motion } from "framer-motion";
import { Search, RotateCcw } from "lucide-react";
import type { FilterState } from "@/types";

interface FilterPanelProps {
  filters: FilterState;
  onChange: (filters: FilterState) => void;
  onReset: () => void;
}

const states = [
  "", "Delhi", "Maharashtra", "Karnataka", "West Bengal", "Tamil Nadu",
  "Telangana", "Gujarat", "Rajasthan", "Uttar Pradesh", "Chandigarh",
  "Madhya Pradesh", "Bihar", "Assam", "Andhra Pradesh",
];

const priorities = ["", "Normal", "Watch", "Alert", "Critical", "Emergency"];

export default function FilterPanel({ filters, onChange, onReset }: FilterPanelProps) {
  const update = (key: keyof FilterState, value: string | number) => {
    onChange({ ...filters, [key]: value });
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: -10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: -10 }}
      className="rounded-2xl p-4 shadow-xl border border-white/5"
      style={{
        background: "rgba(24, 24, 27, 0.85)",
        backdropFilter: "blur(20px)",
      }}
    >
      <div className="flex flex-wrap gap-4 items-end">
        {/* State */}
        <div className="flex-1" style={{ minWidth: 140 }}>
          <label className="text-zinc-500 uppercase tracking-wider mb-1 block font-bold text-[9px]">State</label>
          <select
            value={filters.state}
            onChange={(e) => update("state", e.target.value)}
            className="w-full px-3 py-2 rounded-xl text-xs text-zinc-200 outline-none border border-white/5 bg-zinc-900/40"
          >
            <option value="">All States</option>
            {states.filter(Boolean).map((s) => (
              <option key={s} value={s} className="bg-zinc-900">{s}</option>
            ))}
          </select>
        </div>

        {/* City Search */}
        <div className="flex-1" style={{ minWidth: 140 }}>
          <label className="text-zinc-500 uppercase tracking-wider mb-1 block font-bold text-[9px]">City</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-500" />
            <input
              type="text"
              placeholder="Search city..."
              value={filters.searchCity}
              onChange={(e) => update("searchCity", e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl text-xs text-zinc-200 placeholder-zinc-500 outline-none border border-white/5 bg-zinc-900/40"
            />
          </div>
        </div>

        {/* AQI Range */}
        <div className="flex-1" style={{ minWidth: 180 }}>
          <label className="text-zinc-500 uppercase tracking-wider mb-1 block font-bold text-[9px]">AQI Range: {filters.aqiMin} - {filters.aqiMax}</label>
          <div className="flex gap-3">
            <input
              type="range"
              min={0}
              max={500}
              value={filters.aqiMin}
              onChange={(e) => update("aqiMin", Number(e.target.value))}
              className="flex-1 accent-blue-500 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
            />
            <input
              type="range"
              min={0}
              max={500}
              value={filters.aqiMax}
              onChange={(e) => update("aqiMax", Number(e.target.value))}
              className="flex-1 accent-blue-500 h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>
        </div>

        {/* Priority */}
        <div className="flex-1" style={{ minWidth: 120 }}>
          <label className="text-zinc-500 uppercase tracking-wider mb-1 block font-bold text-[9px]">Priority</label>
          <select
            value={filters.priority}
            onChange={(e) => update("priority", e.target.value)}
            className="w-full px-3 py-2 rounded-xl text-xs text-zinc-200 outline-none border border-white/5 bg-zinc-900/40"
          >
            <option value="">All</option>
            {priorities.filter(Boolean).map((p) => (
              <option key={p} value={p} className="bg-zinc-900">{p}</option>
            ))}
          </select>
        </div>

        {/* Reset */}
        <button
          onClick={onReset}
          className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs text-zinc-400 hover:text-white transition-colors bg-white/5 border border-white/5"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Reset
        </button>
      </div>
    </motion.div>
  );
}
