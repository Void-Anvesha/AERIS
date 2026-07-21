"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts";
import type { ForecastPoint } from "@/types";

interface AqiTrendChartProps {
  data: ForecastPoint[];
}

export default function AqiTrendChart({ data }: AqiTrendChartProps) {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="aqiGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#00E5FF" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#00E5FF" stopOpacity={0} />
          </linearGradient>
        </defs>
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
        <Area type="monotone" dataKey="aqi" stroke="#00E5FF" strokeWidth={2.5} fill="url(#aqiGradient)" dot={false} activeDot={{ r: 5, fill: "#00E5FF", stroke: "#0F172A", strokeWidth: 2 }} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
