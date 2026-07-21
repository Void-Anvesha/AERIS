"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: number;
  icon: ReactNode;
  color: string;
  sparkline?: number[];
  delay?: number;
}

export default function KpiCard({
  title,
  value,
  subtitle,
  trend,
  icon,
  color,
  sparkline,
  delay = 0,
}: KpiCardProps) {
  const trendPositive = trend && trend > 0;
  const trendColor = trendPositive ? "#EF4444" : "#22C55E";

  // Generate sparkline SVG
  const sparklineSvg = sparkline && sparkline.length > 1 ? (() => {
    const min = Math.min(...sparkline);
    const max = Math.max(...sparkline);
    const range = max - min || 1;
    const w = 70;
    const h = 20;
    const points = sparkline
      .map((v, i) => {
        const x = (i / (sparkline.length - 1)) * w;
        const y = h - ((v - min) / range) * (h - 4) - 2;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      })
      .join(" ");
    return { points, w, h };
  })() : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: delay * 0.05 }}
      whileHover={{
        y: -3,
        borderColor: "rgba(255, 255, 255, 0.08)",
        boxShadow: "0 15px 35px -10px rgba(0, 0, 0, 0.6), 0 0 15px rgba(59, 130, 246, 0.03)",
      }}
      className="relative flex flex-col justify-between rounded-2xl p-5 cursor-pointer transition-all duration-300 min-h-[120px]"
      style={{
        background: "rgba(24, 24, 27, 0.6)",
        backdropFilter: "blur(16px)",
        border: "1px solid rgba(255, 255, 255, 0.04)",
      }}
    >
      {/* Background radial glow accent */}
      <div
        className="absolute top-0 right-0 w-24 h-24 rounded-full pointer-events-none opacity-10 blur-2xl"
        style={{ background: color, transform: "translate(15%, -15%)" }}
      />

      {/* Header: Icon + Title */}
      <div className="flex items-center justify-between relative z-10 mb-2">
        <div className="flex items-center gap-2">
          <div
            className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
            style={{ background: `${color}10` }}
          >
            <span style={{ color, scale: 0.85 }}>{icon}</span>
          </div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400">
            {title}
          </span>
        </div>
        {trend !== undefined && (
          <span
            className="inline-flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full"
            style={{
              color: trendColor,
              background: `${trendColor}08`,
            }}
          >
            {trendPositive ? "↑" : "↓"} {Math.abs(trend)}%
          </span>
        )}
      </div>

      {/* Body: Large Value + Sparkline */}
      <div className="flex items-end justify-between relative z-10 mt-auto">
        <div>
          <div className="text-2xl font-bold text-zinc-100 tracking-tight leading-none">
            {value}
          </div>
          {subtitle && (
            <p className="text-[10px] font-medium text-zinc-500 mt-1 leading-tight">
              {subtitle}
            </p>
          )}
        </div>

        {/* Sparkline Chart */}
        {sparklineSvg && (
          <div className="flex-shrink-0 ml-2">
            <svg
              width={sparklineSvg.w}
              height={sparklineSvg.h}
              className="overflow-visible"
            >
              <polyline
                points={sparklineSvg.points}
                fill="none"
                stroke={color}
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        )}
      </div>
    </motion.div>
  );
}
