from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd

from ml.config import RAW_DATA_DIR
from ml.utils import ensure_directory


def discover_data_files(root: str | Path | None = None) -> list[Path]:
    base = Path(root or RAW_DATA_DIR)
    if not base.exists():
        return []
    files = []
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".csv", ".xlsx", ".xls", ".parquet"}:
            files.append(path)
    return files


def load_csv_or_excel(path: str | Path) -> dict[str, pd.DataFrame]:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        return {path.stem: pd.read_csv(path)}
    if path.suffix.lower() in {".xlsx", ".xls"}:
        xls = pd.ExcelFile(path)
        return {sheet: pd.read_excel(path, sheet_name=sheet) for sheet in xls.sheet_names}
    raise ValueError(f"Unsupported file type: {path}")


def build_demo_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    dates = pd.date_range("2024-01-01", periods=40, freq="D")
    aqi_rows = []
    weather_rows = []
    for idx, date in enumerate(dates):
        for city in ["Delhi", "Mumbai", "Bengaluru"]:
            aqi_value = 90 + (idx % 7) * 12 + (0 if city == "Delhi" else 10 if city == "Mumbai" else 5)
            aqi_rows.append({"date": date, "state": "India", "area": city, "aqi_value": aqi_value, "prominent_pollutants": "PM2.5", "air_quality_status": "Moderate"})
            weather_rows.append({"date": date, "state": "India", "location_name": city, "temperature_celsius": 25 + (idx % 5), "humidity": 55 + (idx % 6), "wind_kph": 10 + idx % 8, "pressure_mb": 1005 + idx % 3, "precip_mm": 0.5 if idx % 4 == 0 else 0.0, "cloud": 40 + idx % 10, "visibility_km": 8 + idx % 3, "pm2_5": max(10, aqi_value // 3), "pm10": max(20, aqi_value // 2), "no2": 20 + idx % 10, "so2": 5 + idx % 5, "co": 0.3 + idx % 3 * 0.1, "o3": 40 + idx % 10})
    return pd.DataFrame(aqi_rows), pd.DataFrame(weather_rows)
