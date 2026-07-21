"use client";

export const dynamic = "force-dynamic";

import { useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp } from "lucide-react";
import { useForecast } from "@/hooks/useApi";
import PageHeader from "@/components/shared/PageHeader";
import LoadingSkeleton from "@/components/shared/LoadingSkeleton";
import dynamicComponent from "next/dynamic";

const AqiTrendChart = dynamicComponent(() => import("@/components/charts/AqiTrendChart"), { ssr: false });
const ForecastChart = dynamicComponent(() => import("@/components/charts/ForecastChart"), { ssr: false });
const PollutantPieChart = dynamicComponent(() => import("@/components/charts/PollutantPieChart"), { ssr: false });
const SourceAttributionChart = dynamicComponent(() => import("@/components/charts/SourceAttributionChart"), { ssr: false });

export default function ForecastPage() {
  const { data, isLoading } = useForecast();
  const [trendTab, setTrendTab] = useState<"daily" | "weekly" | "monthly">("daily");
  const [forecastTab, setForecastTab] = useState<"24h" | "48h" | "72h">("24h");

  if (isLoading) {
    return (
      <div className="space-y-4">
        <LoadingSkeleton variant="chart" />
        <LoadingSkeleton variant="chart" />
      </div>
    );
  }

  const trendData = trendTab === "daily" ? data?.daily : trendTab === "weekly" ? data?.weekly : data?.daily;

  const forecastHours = forecastTab === "24h" ? 24 : forecastTab === "48h" ? 48 : 72;
  const forecastData = data?.hourly?.slice(0, forecastHours) || [];

  return (
    <div className="space-y-6 max-w-7xl mx-auto w-full">
      <div className="pb-4 border-b border-white/[0.04]">
        <PageHeader
          title="Forecast & Analytics"
          subtitle="AQI trend streams, machine learning forecasts, and pollutant attribution models"
          icon={<TrendingUp className="w-5 h-5" style={{ color: "#3B82F6" }} />}
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AQI Trend */}
        <ChartCard title="AQI Trend Streams" delay={0}>
          <TabGroup
            tabs={["daily", "weekly", "monthly"]}
            active={trendTab}
            onChange={(t) => setTrendTab(t as typeof trendTab)}
          />
          <AqiTrendChart data={trendData || []} />
        </ChartCard>

        {/* Forecast */}
        <ChartCard title="Predictive AQI Forecast" delay={1}>
          <TabGroup
            tabs={["24h", "48h", "72h"]}
            active={forecastTab}
            onChange={(t) => setForecastTab(t as typeof forecastTab)}
          />
          <ForecastChart data={forecastData} />
        </ChartCard>

        {/* Pollutant Distribution */}
        <ChartCard title="Pollutant Fraction Analysis" delay={2}>
          <PollutantPieChart />
        </ChartCard>

        {/* Source Attribution */}
        <ChartCard title="Emission Source Attribution" delay={3}>
          <SourceAttributionChart />
        </ChartCard>
      </div>
    </div>
  );
}

// Sub-components

function ChartCard({ title, children, delay = 0 }: { title: string; children: React.ReactNode; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: delay * 0.1 }}
      className="rounded-2xl p-5 border border-white/5 shadow-md"
      style={{
        background: "rgba(24, 24, 27, 0.6)",
        backdropFilter: "blur(16px)",
      }}
    >
      <h3 className="text-xs font-bold text-zinc-300 uppercase tracking-wider mb-4">{title}</h3>
      {children}
    </motion.div>
  );
}

function TabGroup({ tabs, active, onChange }: { tabs: string[]; active: string; onChange: (t: string) => void }) {
  return (
    <div className="flex gap-1 mb-4 p-1 rounded-xl w-fit bg-zinc-950/40 border border-white/5">
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => onChange(tab)}
          className="px-3 py-1 rounded-lg text-[10px] font-bold capitalize transition-all"
          style={{
            background: active === tab ? "rgba(59, 130, 246, 0.1)" : "transparent",
            color: active === tab ? "#3B82F6" : "#71717A",
          }}
        >
          {tab}
        </button>
      ))}
    </div>
  );
}
