import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// ===== AQI Utilities =====

export type AqiCategory = "good" | "moderate" | "unhealthy-sg" | "unhealthy" | "very-unhealthy" | "hazardous";

export function getAqiCategory(aqi: number): AqiCategory {
  if (aqi <= 50) return "good";
  if (aqi <= 100) return "moderate";
  if (aqi <= 150) return "unhealthy-sg";
  if (aqi <= 200) return "unhealthy";
  if (aqi <= 300) return "very-unhealthy";
  return "hazardous";
}

export function getAqiColor(aqi: number): string {
  if (aqi <= 50) return "#22C55E";
  if (aqi <= 100) return "#F59E0B";
  if (aqi <= 200) return "#F97316";
  if (aqi <= 300) return "#EF4444";
  return "#A855F7";
}

export function getAqiLabel(aqi: number): string {
  if (aqi <= 50) return "Good";
  if (aqi <= 100) return "Moderate";
  if (aqi <= 150) return "Unhealthy for Sensitive Groups";
  if (aqi <= 200) return "Unhealthy";
  if (aqi <= 300) return "Very Unhealthy";
  return "Hazardous";
}

export function getAqiBgClass(aqi: number): string {
  if (aqi <= 50) return "bg-green-500/15 text-green-400 border-green-500/30";
  if (aqi <= 100) return "bg-yellow-500/15 text-yellow-400 border-yellow-500/30";
  if (aqi <= 200) return "bg-orange-500/15 text-orange-400 border-orange-500/30";
  if (aqi <= 300) return "bg-red-500/15 text-red-400 border-red-500/30";
  return "bg-purple-500/15 text-purple-400 border-purple-500/30";
}

export function formatNumber(num: number): string {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
  if (num >= 1000) return (num / 1000).toFixed(1) + "K";
  return num.toString();
}

export function getHealthRisk(aqi: number): string {
  if (aqi <= 50) return "Low";
  if (aqi <= 100) return "Moderate";
  if (aqi <= 200) return "High";
  if (aqi <= 300) return "Very High";
  return "Severe";
}

export function getPriorityLevel(aqi: number): string {
  if (aqi <= 50) return "Normal";
  if (aqi <= 100) return "Watch";
  if (aqi <= 200) return "Alert";
  if (aqi <= 300) return "Critical";
  return "Emergency";
}
