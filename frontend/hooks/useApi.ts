"use client";

import { useQuery } from "@tanstack/react-query";
import { getDashboard, getLocations, getForecast, getHotspots, getAdvisory } from "@/services/api";

export function useDashboard() {
  return useQuery({
    queryKey: ["dashboard"],
    queryFn: getDashboard,
    refetchInterval: 30000,
  });
}

export function useLocations() {
  return useQuery({
    queryKey: ["locations"],
    queryFn: getLocations,
    refetchInterval: 60000,
  });
}

export function useForecast(city?: string) {
  return useQuery({
    queryKey: ["forecast", city],
    queryFn: () => getForecast(city),
  });
}

export function useHotspots() {
  return useQuery({
    queryKey: ["hotspots"],
    queryFn: getHotspots,
  });
}

export function useAdvisory() {
  return useQuery({
    queryKey: ["advisory"],
    queryFn: getAdvisory,
  });
}
