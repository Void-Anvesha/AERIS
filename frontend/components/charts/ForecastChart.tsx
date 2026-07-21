"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";
import type { ForecastPoint } from "@/types";

interface ForecastChartProps {
  data: ForecastPoint[];
}

export default function ForecastChart({ data }: ForecastChartProps) {
  // Sample every nth point for readability
  const step = Math.max(1, Math.floor(data.length / 24));
  const sampled = data.filter((_, i) => i % step === 0);

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={sampled}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.06)" />
        <XAxis dataKey="time" tick={{ fill: "#64748B", fontSize: 11 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: "#64748B", fontSize: 11 }} axisLine={false} tickLine={false} />
        <Tooltip
          contentStyle={{
            background: "rgba(30, 41, 59, 0.95)",
            border: "1px solid rgba(148, 163, 184, 0.1)",
            borderRadius: 12,
            color: "#F8FAFC",
            fontSize: 12,
            boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
          }}
        />
        <Legend wrapperStyle={{ fontSize: 11, color: "#94A3B8" }} />
        <Line type="monotone" dataKey="aqi" name="AQI" stroke="#00E5FF" strokeWidth={2} dot={false} />
        <Line type="monotone" dataKey="pm25" name="PM2.5" stroke="#EF4444" strokeWidth={1.5} dot={false} strokeDasharray="5 5" />
        <Line type="monotone" dataKey="pm10" name="PM10" stroke="#F97316" strokeWidth={1.5} dot={false} strokeDasharray="5 5" />
      </LineChart>
    </ResponsiveContainer>
  );
}
