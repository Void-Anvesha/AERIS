from __future__ import annotations

from typing import Any

import pandas as pd


class DataFusionAgent:
    """Merge air quality, weather, and contextual datasets into a unified frame."""

    def __init__(self) -> None:
        self._required_columns = {
            "aqi": ["date", "city", "aqi"],
            "weather": ["date", "city", "temperature", "humidity"],
            "traffic": ["date", "city", "traffic_index"],
        }

    def run(self, aqi_df: pd.DataFrame, weather_df: pd.DataFrame, traffic_df: pd.DataFrame) -> pd.DataFrame:
        self._validate_required_columns(aqi_df, weather_df, traffic_df)

        merged = self._merge_datasets(aqi_df, weather_df, traffic_df)
        merged = self._normalize_schema(merged)
        merged = self._handle_missing_values(merged)
        merged = self._deduplicate(merged)

        if merged.empty:
            raise ValueError("DataFusionAgent produced an empty dataset after merging.")

        return merged

    def _validate_required_columns(self, aqi_df: pd.DataFrame, weather_df: pd.DataFrame, traffic_df: pd.DataFrame) -> None:
        missing_columns = []
        for dataset_name, required_columns in self._required_columns.items():
            df = {
                "aqi": aqi_df,
                "weather": weather_df,
                "traffic": traffic_df,
            }[dataset_name]
            missing = [column for column in required_columns if column not in df.columns]
            if missing:
                missing_columns.append(f"{dataset_name}: {missing}")

        if missing_columns:
            raise ValueError(f"Missing required columns in input datasets: {', '.join(missing_columns)}")

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
        merged["aqi"] = pd.to_numeric(merged.get("aqi", 0), errors="coerce")
        merged["temperature"] = pd.to_numeric(merged.get("temperature", 0), errors="coerce")
        merged["humidity"] = pd.to_numeric(merged.get("humidity", 0), errors="coerce")
        merged["traffic_index"] = pd.to_numeric(merged.get("traffic_index", 0), errors="coerce")
        return merged

    def _handle_missing_values(self, merged: pd.DataFrame) -> pd.DataFrame:
        defaults = {
            "aqi": 0.0,
            "temperature": 0.0,
            "humidity": 0.0,
            "traffic_index": 0.0,
            "industrial_score": 0.0,
            "green_cover": 0.0,
        }
        for column, default in defaults.items():
            if column not in merged.columns:
                merged[column] = default
        merged = merged.fillna(defaults)
        return merged

    def _deduplicate(self, merged: pd.DataFrame) -> pd.DataFrame:
        return merged.drop_duplicates(subset=["date", "city"], keep="last").reset_index(drop=True)
