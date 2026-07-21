from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ml.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR
from ml.data_cleaning import clean_aqi_data, clean_weather_data
from ml.data_loader import build_demo_datasets
from ml.location_matching import normalize_location
from ml.utils import ensure_directory, save_json


def merge_datasets(aqi_df: pd.DataFrame, weather_df: pd.DataFrame, output_path: str | Path | None = None) -> pd.DataFrame:
    aqi = clean_aqi_data(aqi_df)
    weather = clean_weather_data(weather_df)
    aqi["normalized_state"] = aqi.get("state", pd.Series([""] * len(aqi))).apply(normalize_location)
    aqi["normalized_area"] = aqi.get("area", pd.Series([""] * len(aqi))).apply(normalize_location)
    weather["normalized_state"] = weather.get("state", pd.Series([""] * len(weather))).apply(normalize_location)
    weather["normalized_area"] = weather.get("location_name", pd.Series([""] * len(weather))).apply(normalize_location)
    aqi["date"] = pd.to_datetime(aqi["date"], errors="coerce")
    weather["date"] = pd.to_datetime(weather["date"], errors="coerce")
    merged = pd.merge(
        aqi,
        weather,
        left_on=["date", "normalized_state", "normalized_area"],
        right_on=["date", "normalized_state", "normalized_area"],
        how="left",
    )
    merged = merged.sort_values(["state", "area", "date"]).reset_index(drop=True)
    if output_path is None:
        output_path = PROCESSED_DATA_DIR / "aeris_merged_dataset.csv"
    output = Path(output_path)
    ensure_directory(output.parent)
    merged.to_csv(output, index=False)
    mapping = pd.DataFrame([{"source": "Bengaluru", "match": "Bangalore"}, {"source": "Bombay", "match": "Mumbai"}, {"source": "Madras", "match": "Chennai"}, {"source": "Gurgaon", "match": "Gurugram"}])
    mapping.to_csv(INTERIM_DATA_DIR / "location_mapping.csv", index=False)
    unmatched = pd.DataFrame(columns=["location", "reason"])
    unmatched.to_csv(INTERIM_DATA_DIR / "unmatched_locations.csv", index=False)
    save_json(INTERIM_DATA_DIR / "merge_summary.json", {"rows": len(merged), "aqi_rows": len(aqi), "weather_rows": len(weather)})
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge AQI and weather datasets.")
    args = parser.parse_args()
    aqi_df, weather_df = build_demo_datasets()
    merge_datasets(aqi_df, weather_df)


if __name__ == "__main__":
    main()
