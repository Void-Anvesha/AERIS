from __future__ import annotations

import pandas as pd

from ml.utils import normalize_text, parse_date


def validate_aqi_series(values: pd.Series | list[float]) -> pd.Series:
    series = pd.Series(values, copy=True)
    series = pd.to_numeric(series, errors="coerce")
    series = series[(series >= 0) & (series <= 500)]
    return series


def clean_aqi_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["date"] = cleaned["date"].apply(parse_date)
    cleaned = cleaned.dropna(subset=["date"])
    cleaned["aqi_value"] = pd.to_numeric(cleaned.get("aqi_value", pd.Series([None] * len(cleaned))), errors="coerce")
    cleaned = cleaned.dropna(subset=["aqi_value"])
    cleaned = cleaned[(cleaned["aqi_value"] >= 0) & (cleaned["aqi_value"] <= 500)]
    for column in ["state", "area", "prominent_pollutants"]:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna("").astype(str).str.strip()
            cleaned[column] = cleaned[column].str.title()
    cleaned = cleaned.drop_duplicates(subset=["state", "area", "date"], keep="last")
    cleaned = cleaned.sort_values(["state", "area", "date"]).reset_index(drop=True)
    for column in ["unit", "note"]:
        if column in cleaned.columns:
            fill_ratio = cleaned[column].isna().mean()
            if fill_ratio > 0.9:
                cleaned = cleaned.drop(columns=[column])
    return cleaned


def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["date"] = cleaned["date"].apply(parse_date)
    cleaned = cleaned.dropna(subset=["date"])
    for column in ["temperature_fahrenheit", "temp_f"]:
        if column in cleaned.columns and "temperature_celsius" in cleaned.columns:
            cleaned = cleaned.drop(columns=[column])
    for column in ["wind_mph", "gust_mph"]:
        if column in cleaned.columns and "wind_kph" in cleaned.columns:
            cleaned = cleaned.drop(columns=[column])
    for column in ["pressure_in", "pressure_inches"]:
        if column in cleaned.columns and "pressure_mb" in cleaned.columns:
            cleaned = cleaned.drop(columns=[column])
    for column in ["precip_in", "rain_inches"]:
        if column in cleaned.columns and "precip_mm" in cleaned.columns:
            cleaned = cleaned.drop(columns=[column])
    for column in ["visibility_miles", "visibility_mi"]:
        if column in cleaned.columns and "visibility_km" in cleaned.columns:
            cleaned = cleaned.drop(columns=[column])
    numeric_columns = [c for c in cleaned.columns if c not in {"date", "location_name", "region", "state", "area", "last_updated", "location", "name"}]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    if "humidity" in cleaned.columns:
        cleaned["humidity"] = cleaned["humidity"].clip(lower=0, upper=100)
    if "latitude" in cleaned.columns:
        cleaned["latitude"] = cleaned["latitude"].clip(lower=-90, upper=90)
    if "longitude" in cleaned.columns:
        cleaned["longitude"] = cleaned["longitude"].clip(lower=-180, upper=180)
    cleaned = cleaned.drop_duplicates(subset=["date", "location_name"], keep="last")
    cleaned = cleaned.sort_values(["location_name", "date"]).reset_index(drop=True)
    return cleaned
