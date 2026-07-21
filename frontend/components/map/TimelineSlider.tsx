"use client";

import { motion } from "framer-motion";
import type { TimelinePosition } from "@/types";

interface TimelineSliderProps {
  value: TimelinePosition;
  onChange: (position: TimelinePosition) => void;
}

const positions: { key: TimelinePosition; label: string }[] = [
  { key: "yesterday", label: "Yesterday" },
  { key: "today", label: "Today" },
  { key: "tomorrow", label: "Tomorrow" },
  { key: "72hours", label: "72 Hours" },
  { key: "nextweek", label: "Next Week" },
];

export default function TimelineSlider({ value, onChange }: TimelineSliderProps) {
  const activeIndex = positions.findIndex((p) => p.key === value);

  return (
    <div
      className="rounded-2xl p-4 flex items-center gap-1 border border-white/5 shadow-lg"
      style={{
        background: "rgba(24, 24, 27, 0.85)",
        backdropFilter: "blur(20px)",
      }}
    >
      <span className="text-zinc-500 uppercase tracking-wider mr-4 font-bold text-[9px]">
        Timeline
      </span>

      {/* Track with dots */}
      <div className="flex-1 relative flex items-center">
        {/* Background track */}
        <div className="absolute left-0 right-0 h-0.5 rounded-full" style={{ background: "rgba(255, 255, 255, 0.05)" }} />

        {/* Active track */}
        <motion.div
          className="absolute left-0 h-0.5 rounded-full"
          style={{ background: "#3B82F6" }}
          animate={{ width: `${(activeIndex / (positions.length - 1)) * 100}%` }}
          transition={{ duration: 0.3 }}
        />

        {/* Position buttons */}
        <div className="relative flex justify-between w-full">
          {positions.map((pos, i) => {
            const isActive = pos.key === value;
            const isPast = i <= activeIndex;

            return (
              <button
                key={pos.key}
                onClick={() => onChange(pos.key)}
                className="flex flex-col items-center gap-2 group relative z-10"
              >
                <motion.div
                  whileHover={{ scale: 1.25 }}
                  className="w-2.5 h-2.5 rounded-full border transition-colors"
                  style={{
                    background: isActive ? "#3B82F6" : isPast ? "#3B82F6" : "transparent",
                    borderColor: isPast ? "#3B82F6" : "rgba(255, 255, 255, 0.15)",
                    boxShadow: isActive ? "0 0 10px rgba(59, 130, 246, 0.5)" : "none",
                  }}
                />
                <span
                  className="font-semibold transition-colors text-[10px]"
                  style={{ color: isActive ? "#3B82F6" : isPast ? "#A1A1AA" : "#52525B" }}
                >
                  {pos.label}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
