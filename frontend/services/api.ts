import type { Location, DashboardData, ForecastData, Hotspot, AdvisoryData } from "@/types";
import {
  mockLocations,
  mockDashboard,
  mockForecast,
  mockHotspots,
  mockAdvisory,
  mockChatResponses,
} from "./mockData";

// Simulate network delay
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

// GET /dashboard
export async function getDashboard(): Promise<DashboardData> {
  await delay(600);
  return mockDashboard;
}

// GET /locations
export async function getLocations(): Promise<Location[]> {
  await delay(800);
  return mockLocations;
}

// GET /forecast?city=
export async function getForecast(city?: string): Promise<ForecastData> {
  await delay(700);
  if (city) {
    const loc = mockLocations.find((l) => l.city.toLowerCase() === city.toLowerCase());
    if (loc) {
      return { ...mockForecast, city: loc.city };
    }
  }
  return mockForecast;
}

// GET /hotspots
export async function getHotspots(): Promise<Hotspot[]> {
  await delay(500);
  return mockHotspots;
}

// GET /advisory
export async function getAdvisory(): Promise<AdvisoryData> {
  await delay(400);
  return mockAdvisory;
}

// GET /recommendation?locationId=
export async function getRecommendation(locationId: string): Promise<{ recommendation: string }> {
  await delay(300);
  const loc = mockLocations.find((l) => l.id === locationId);
  return { recommendation: loc?.recommendation || "No recommendation available." };
}

// POST /chat
export async function sendChatMessage(message: string): Promise<string> {
  try {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (res.ok) {
      const data = await res.json();
      if (data.response) return data.response;
    }
  } catch (err) {
    console.warn("Backend chat endpoint failed, falling back to mock response", err);
  }

  // Fallback to intelligent mock response if backend fails
  await delay(1000);
  const lower = message.toLowerCase();
  if (lower.includes("why") || lower.includes("increase")) return mockChatResponses["why"];
  if (lower.includes("which") || lower.includes("inspection")) return mockChatResponses["which"];
  if (lower.includes("what") || lower.includes("cause")) return mockChatResponses["what"];
  if (lower.includes("how") || lower.includes("reduce") || lower.includes("authorities")) return mockChatResponses["how"];
  return mockChatResponses["default"];
}


// ===== Real-Time AI Agent APIs =====

export interface InsightInput {
  aqi: number;
  forecast: number;
  confidence: number;
  dominant_pollutant: string;
  source: string;
  hotspot: boolean;
  nearby_schools: number;
  nearby_hospitals: number;
  population_density: "Low" | "Medium" | "High";
  zone_name?: string;
}

export interface DecisionOutput {
  risk_score: number;
  priority: "Low" | "Medium" | "High" | "Critical";
  authority: string;
  response_time: string;
  recommended_actions: string[];
  reason: string[];
  manual_review_required: boolean;
  aqi: number;
  forecast: number;
  dominant_pollutant: string;
  source: string;
  zone_name?: string;
}

export interface AdvisoryResponse {
  authority_advisory: string;
  citizen_advisory: string;
}

export async function runDecision(insight: InsightInput): Promise<DecisionOutput> {
  const res = await fetch("http://localhost:8000/api/agents/decision", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(insight),
  });
  if (!res.ok) throw new Error("Failed to evaluate Decision Intelligence Model");
  return res.json();
}

export async function runAdvisory(decision: DecisionOutput): Promise<AdvisoryResponse> {
  const res = await fetch("http://localhost:8000/api/agents/advisory", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(decision),
  });
  if (!res.ok) throw new Error("Failed to generate LLM Advisory");
  return res.json();
}
