"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const data = [
  { name: "Traffic", value: 35, color: "#00E5FF" },
  { name: "Industry", value: 20, color: "#A855F7" },
  { name: "Construction", value: 18, color: "#F97316" },
  { name: "Crop Burning", value: 15, color: "#EF4444" },
  { name: "Fire", value: 5, color: "#F59E0B" },
  { name: "Dust", value: 7, color: "#78716C" },
];

export default function SourceAttributionChart() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={65}
          outerRadius={100}
          paddingAngle={4}
          dataKey="value"
          stroke="none"
        >
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            background: "rgba(30, 41, 59, 0.95)",
            border: "1px solid rgba(148, 163, 184, 0.1)",
            borderRadius: 12,
            color: "#F8FAFC",
            fontSize: 12,
            boxShadow: "0 8px 32px rgba(0,0,0,0.3)",
          }}
          formatter={(value: number) => [`${value}%`, ""]}
        />
        <Legend
          wrapperStyle={{ fontSize: 11 }}
          formatter={(value: string) => <span style={{ color: "#94A3B8" }}>{value}</span>}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
