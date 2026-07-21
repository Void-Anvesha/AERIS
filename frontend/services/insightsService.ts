import { fetchJson } from '@/lib/api';

export interface InsightSummary {
  city: string;
  current_aqi: number;
  status: string;
  trend: string;
  forecast_next_24h: number;
  forecast_next_72h: number;
  recommendation: string;
  advisory: string;
}

export async function getInsights(): Promise<InsightSummary> {
  return fetchJson<InsightSummary>('/insights');
}
