"use client";

import { useInsights } from '@/hooks/useInsights';
import { InsightSummary } from '@/services/insightsService';

export default function DashboardPage() {
  const { data, loading, error } = useInsights<InsightSummary>('/insights');

  if (loading) return <p>Loading dashboard foundation...</p>;
  if (error) return <p>{error}</p>;

  return (
    <main style={{ padding: 24 }}>
      <h1>AERIS Dashboard Foundation</h1>
      <p>City: {data?.city}</p>
      <p>Current AQI: {data?.current_aqi}</p>
      <p>Status: {data?.status}</p>
    </main>
  );
}
