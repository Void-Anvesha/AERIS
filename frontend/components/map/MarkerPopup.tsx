"use client";

import type { Location } from "@/types";
import { getAqiColor, getAqiLabel } from "@/lib/utils";

interface MarkerPopupProps {
  location: Location;
}

export default function MarkerPopup({ location }: MarkerPopupProps) {
  const aqiColor = getAqiColor(location.currentAqi);

  return (
    <div style={{ fontFamily: "'Inter', sans-serif", minWidth: 260, padding: "16px" }}>
      {/* City Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
        <div>
          <h3 style={{ color: "#F8FAFC", fontSize: 16, fontWeight: 700, margin: 0 }}>
            {location.city}
          </h3>
          <p style={{ color: "#64748B", fontSize: 11, margin: "2px 0 0" }}>
            {location.latitude.toFixed(4)}°N, {location.longitude.toFixed(4)}°E
          </p>
        </div>
        <div
          style={{
            width: 48,
            height: 48,
            borderRadius: 12,
            background: `${aqiColor}20`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
          }}
        >
          <span style={{ color: aqiColor, fontSize: 18, fontWeight: 800, lineHeight: 1 }}>
            {location.currentAqi}
          </span>
          <span style={{ color: aqiColor, fontSize: 8, fontWeight: 600, textTransform: "uppercase" }}>
            AQI
          </span>
        </div>
      </div>

      {/* Status Badge */}
      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 6,
          padding: "4px 10px",
          borderRadius: 8,
          background: `${aqiColor}15`,
          marginBottom: 12,
        }}
      >
        <div style={{ width: 6, height: 6, borderRadius: "50%", background: aqiColor }} />
        <span style={{ color: aqiColor, fontSize: 11, fontWeight: 600 }}>
          {getAqiLabel(location.currentAqi)}
        </span>
      </div>

      {/* Info Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 8,
          marginBottom: 12,
        }}
      >
        {[
          { label: "Forecast", value: location.forecastAqi, unit: "AQI" },
          { label: "Temperature", value: `${location.temperature}°C`, unit: "" },
          { label: "Humidity", value: `${location.humidity}%`, unit: "" },
          { label: "Pollutant", value: location.dominantPollutant, unit: "" },
          { label: "Confidence", value: `${location.confidenceScore}%`, unit: "" },
          { label: "Priority", value: location.priorityLevel, unit: "" },
        ].map((item) => (
          <div
            key={item.label}
            style={{
              padding: "8px 10px",
              borderRadius: 8,
              background: "rgba(148, 163, 184, 0.06)",
            }}
          >
            <p style={{ color: "#64748B", fontSize: 10, margin: 0, textTransform: "uppercase", letterSpacing: 0.5 }}>
              {item.label}
            </p>
            <p style={{ color: "#F8FAFC", fontSize: 13, fontWeight: 600, margin: "2px 0 0" }}>
              {item.value} {item.unit}
            </p>
          </div>
        ))}
      </div>

      {/* Recommendation */}
      <div
        style={{
          padding: "10px 12px",
          borderRadius: 8,
          background: "rgba(0, 229, 255, 0.06)",
          borderLeft: "3px solid #00E5FF",
        }}
      >
        <p style={{ color: "#64748B", fontSize: 10, margin: 0, textTransform: "uppercase", letterSpacing: 0.5 }}>
          Recommendation
        </p>
        <p style={{ color: "#94A3B8", fontSize: 12, margin: "4px 0 0", lineHeight: 1.4 }}>
          {location.recommendation}
        </p>
      </div>
    </div>
  );
}
