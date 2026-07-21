from __future__ import annotations

from typing import Any

import pandas as pd


class DataFusionAgent:
    """Merge air quality, weather, and contextual datasets into a unified frame."""

    def __init__(self) -> None:
        self._required_columns = {"aqi": ["date", "city", "aqi"], "weather": ["date", "city", "temperature", "humidity"], "traffic": ["date", "city", "traffic_index"]}

    def run(self, aqi_df: pd.DataFrame, weather_df: pd.DataFrame, traffic_df: pd.DataFrame) -> pd.DataFrame:
        merged = self._merge_datasets(aqi_df, weather_df, traffic_df)
        merged = self._normalize_schema(merged)
        merged = self._handle_missing_values(merged)
        return merged

    def _merge_datasets(self, aqi_df: pd.DataFrame, weather_df: pd.DataFrame, traffic_df: pd.DataFrame) -> pd.DataFrame:
        aqi_df = aqi_df.copy()
        weather_df = weather_df.copy()
        traffic_df = traffic_df.copy()

        aqi_df["date"] = pd.to_datetime(aqi_df["date"], errors="coerce")
        weather_df["date"] = pd.to_datetime(weather_df["date"], errors="coerce")
        traffic_df["date"] = pd.to_datetime(traffic_df["date"], errors="coerce")

        aqi_df["city"] = aqi_df["city"].astype(str).str.strip().str.title()
        weather_df["city"] = weather_df["city"].astype(str).str.strip().str.title()
        traffic_df["city"] = traffic_df["city"].astype(str).str.strip().str.title()

        merged = pd.merge(aqi_df, weather_df, on=["date", "city"], how="left")
        merged = pd.merge(merged, traffic_df, on=["date", "city"], how="left")
        return merged

    def _normalize_schema(self, merged: pd.DataFrame) -> pd.DataFrame:
        merged = merged.sort_values(["city", "date"]).reset_index(drop=True)
        merged["date"] = pd.to_datetime(merged["date"], errors="coerce")
        merged["city"] = merged["city"].fillna("Unknown").astype(str).str.title()
        return merged

    def _handle_missing_values(self, merged: pd.DataFrame) -> pd.DataFrame:
        numeric_columns = [col for col in merged.columns if col not in {"date", "city"}]
        for col in numeric_columns:
            merged[col] = pd.to_numeric(merged[col], errors="coerce")
        merged = merged.fillna({
            "temperature": 0.0,
            "humidity": 0.0,
            "traffic_index": 0.0,
            "aqi": 0.0,
        })
        return merged
