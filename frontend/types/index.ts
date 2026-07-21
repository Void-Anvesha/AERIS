// ===== Core Domain Types =====

export interface Location {
  id: string;
  city: string;
  state: string;
  ward?: string;
  latitude: number;
  longitude: number;
  currentAqi: number;
  forecastAqi: number;
  temperature: number;
  humidity: number;
  windSpeed: number;
  rainfall: number;
  dominantPollutant: string;
  confidenceScore: number;
  priorityLevel: "Normal" | "Watch" | "Alert" | "Critical" | "Emergency";
  recommendation: string;
  pollutants: Pollutants;
  nearbyRoads: number;
  nearbySchools: number;
  nearbyHospitals: number;
  nearbyIndustries: number;
  nearbyConstructionSites: number;
  greenCoverPercent: number;
  healthRisk: "Low" | "Moderate" | "High" | "Very High" | "Severe";
  sources: SourceAttribution;
}

export interface Pollutants {
  pm25: number;
  pm10: number;
  no2: number;
  co: number;
  so2: number;
  o3: number;
}

export interface SourceAttribution {
  traffic: number;
  industry: number;
  construction: number;
  cropBurning: number;
  fire: number;
  dust: number;
}

// ===== Dashboard =====

export interface DashboardData {
  currentAqi: number;
  averageAqi: number;
  highRiskAreas: number;
  activeAlerts: number;
  worstCity: string;
  worstCityAqi: number;
  monitoringStations: number;
  trends: {
    currentAqiTrend: number;
    averageAqiTrend: number;
    highRiskTrend: number;
    alertsTrend: number;
  };
  sparklines: {
    currentAqi: number[];
    averageAqi: number[];
    highRisk: number[];
    alerts: number[];
  };
  recentAlerts: Alert[];
}

export interface Alert {
  id: string;
  city: string;
  state: string;
  message: string;
  severity: "info" | "warning" | "danger" | "critical";
  timestamp: string;
}

// ===== Forecast =====

export interface ForecastPoint {
  time: string;
  aqi: number;
  pm25: number;
  pm10: number;
  no2?: number;
  co?: number;
  so2?: number;
}

export interface ForecastData {
  city: string;
  hourly: ForecastPoint[];
  daily: ForecastPoint[];
  weekly: ForecastPoint[];
}

// ===== Hotspots =====

export interface Hotspot {
  rank: number;
  latitude: number;
  longitude: number;
  city: string;
  state: string;
  aqi: number;
  forecastAqi: number;
  risk: "High" | "Very High" | "Severe";
  reason: string;
  action: string;
}

// ===== Chat =====

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

// ===== Advisory =====

export interface AdvisoryData {
  currentAqi: number;
  healthRisk: string;
  generalAdvice: string;
  recommendations: AdvisoryRecommendation[];
}

export interface AdvisoryRecommendation {
  id: string;
  icon: string;
  category: "general" | "elderly" | "children" | "outdoor" | "schools" | "medical";
  title: string;
  description: string;
  severity: "low" | "moderate" | "high" | "critical";
}

// ===== Filters =====

export interface FilterState {
  state: string;
  city: string;
  aqiMin: number;
  aqiMax: number;
  pollutant: string;
  date: string;
  season: string;
  priority: string;
  searchCoords: string;
  searchCity: string;
}

// ===== Timeline =====

export type TimelinePosition = "yesterday" | "today" | "tomorrow" | "72hours" | "nextweek";

// ===== Map Layer =====

export type MapLayer = "markers" | "heatmap" | "satellite" | "terrain";
