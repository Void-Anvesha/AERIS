"use client";

import { motion } from "framer-motion";
import type { Alert } from "@/types";
import { AlertTriangle, Bell, ShieldAlert, Info, ArrowUpRight } from "lucide-react";
import Link from "next/link";

interface AlertsFeedProps {
  alerts: Alert[];
}

const severityConfig = {
  info: { color: "#3B82F6", bg: "rgba(59, 130, 246, 0.08)", label: "INFO", icon: Info },
  warning: { color: "#F59E0B", bg: "rgba(245, 158, 11, 0.08)", label: "WARN", icon: AlertTriangle },
  danger: { color: "#EF4444", bg: "rgba(239, 68, 68, 0.08)", label: "HIGH", icon: ShieldAlert },
  critical: { color: "#A855F7", bg: "rgba(168, 85, 247, 0.08)", label: "CRIT", icon: ShieldAlert },
};

export default function AlertsFeed({ alerts }: AlertsFeedProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="rounded-2xl overflow-hidden flex flex-col h-full"
      style={{
        background: "rgba(24, 24, 27, 0.6)",
        backdropFilter: "blur(16px)",
        border: "1px solid rgba(255, 255, 255, 0.04)",
      }}
    >
      <div className="px-5 py-4 border-b border-white/[0.04] flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl" style={{ background: "rgba(239, 68, 68, 0.08)", color: "#EF4444" }}>
            <Bell className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider">Live Alert Feed</h3>
            <p className="text-[10px] text-zinc-500 font-medium">IoT sensor & anomaly events</p>
          </div>
        </div>
        <span
          className="text-[10px] px-2 py-0.5 rounded-full font-bold bg-red-500/10 text-red-400"
        >
          {alerts.length} Active
        </span>
      </div>

      <div className="flex-1 overflow-y-auto divide-y divide-white/[0.02] p-1.5">
        {alerts.map((alert, i) => {
          const config = severityConfig[alert.severity] || severityConfig.warning;
          const IconComp = config.icon;

          return (
            <motion.div
              key={alert.id}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.05 * i }}
              className="flex items-start gap-3.5 px-3 py-3 hover:bg-white/[0.02] cursor-pointer transition-all rounded-xl group"
            >
              <div
                className="w-7.5 h-7.5 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                style={{ background: config.bg, border: `1px solid ${config.color}15` }}
              >
                <IconComp className="w-3.5 h-3.5" style={{ color: config.color }} />
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold text-zinc-200 group-hover:text-blue-400 transition-colors">
                      {alert.city}, {alert.state}
                    </span>
                    <span
                      className="font-bold px-1 py-0.2 rounded text-[8px] uppercase tracking-wider"
                      style={{ background: config.bg, color: config.color, border: `1px solid ${config.color}15` }}
                    >
                      {config.label}
                    </span>
                  </div>
                  <span className="text-[9px] text-zinc-500 font-medium whitespace-nowrap">
                    {alert.timestamp}
                  </span>
                </div>
                <p className="text-[11px] text-zinc-400 leading-normal font-normal">{alert.message}</p>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="p-3 border-t border-white/[0.04] text-center flex-shrink-0">
        <Link href="/hotspots">
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-400 hover:text-blue-300 transition-colors cursor-pointer">
            View All Hotspot Logs
            <ArrowUpRight className="w-3 h-3" />
          </span>
        </Link>
      </div>
    </motion.div>
  );
}
