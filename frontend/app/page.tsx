"use client";

import { useEffect, useState } from 'react';

interface Insight {
  city: string;
  current_aqi: number;
  status: string;
  trend: string;
  forecast_next_24h: number;
  forecast_next_72h: number;
  recommendation: string;
  advisory: string;
}

export default function HomePage() {
  const [insight, setInsight] = useState<Insight | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/insights')
      .then((res) => res.json())
      .then((data) => setInsight(data));
  }, []);

  return (
    <main className="container">
      <h1 style={{ fontSize: '2rem', marginBottom: '12px' }}>AERIS</h1>
      <p style={{ color: '#9fb3cc' }}>AI Powered Urban Air Quality Intelligence Platform</p>

      {insight ? (
        <div style={{ display: 'grid', gap: '16px', marginTop: '24px' }}>
          <section className="card">
            <h2>Current Situation</h2>
            <p>City: {insight.city}</p>
            <p>Current AQI: {insight.current_aqi}</p>
            <p>Status: {insight.status}</p>
            <p>Trend: {insight.trend}</p>
          </section>

          <section className="card">
            <h2>Forecast</h2>
            <p>Next 24h: {insight.forecast_next_24h}</p>
            <p>Next 72h: {insight.forecast_next_72h}</p>
          </section>

          <section className="card">
            <h2>Recommended Action</h2>
            <p>{insight.recommendation}</p>
          </section>

          <section className="card">
            <h2>Citizen Advisory</h2>
            <p>{insight.advisory}</p>
          </section>
        </div>
      ) : (
        <p>Loading intelligence snapshot...</p>
      )}
    </main>
  );
}
