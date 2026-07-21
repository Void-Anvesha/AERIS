"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const data = [
  { name: "PM2.5", value: 35, color: "#EF4444" },
  { name: "PM10", value: 28, color: "#F97316" },
  { name: "NO₂", value: 15, color: "#F59E0B" },
  { name: "CO", value: 10, color: "#A855F7" },
  { name: "SO₂", value: 7, color: "#3B82F6" },
  { name: "O₃", value: 5, color: "#22C55E" },
];

export default function PollutantPieChart() {
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
