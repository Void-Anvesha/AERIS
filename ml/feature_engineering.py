from __future__ import annotations

import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    sort_columns = [col for col in ["state", "area", "date"] if col in out.columns]
    if sort_columns:
        out = out.sort_values(sort_columns).reset_index(drop=True)
    else:
        out = out.reset_index(drop=True)
    if "date" not in out.columns:
        out["date"] = pd.date_range("2024-01-01", periods=len(out), freq="D")
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    out["day"] = out["date"].dt.day
    out["day_of_week"] = out["date"].dt.dayofweek
    out["day_of_year"] = out["date"].dt.dayofyear
    out["week_of_year"] = out["date"].dt.isocalendar().week.astype(int)
    out["quarter"] = out["date"].dt.quarter
    out["is_weekend"] = out["day_of_week"].isin([5, 6]).astype(int)

    season_labels = ["Winter", "Summer", "Monsoon", "Post-Monsoon", "Winter"]
    season_bins = [0, 2, 5, 9, 11, 12]
    season_codes = pd.cut(
        out["month"],
        bins=season_bins,
        labels=list(range(len(season_labels))),
        include_lowest=True,
    )
    out["season"] = season_codes.map({i: label for i, label in enumerate(season_labels)})
    return out


def add_lag_features(df: pd.DataFrame, group_cols: list[str], target_col: str = "aqi_value") -> pd.DataFrame:
    out = df.copy()
    sort_columns = [col for col in group_cols + ["date"] if col in out.columns]
    if sort_columns:
        out = out.sort_values(sort_columns).reset_index(drop=True)
    else:
        out = out.reset_index(drop=True)
    for lag in [1, 2, 3, 7]:
        if all(col in out.columns for col in group_cols):
            out[f"aqi_lag_{lag}"] = out.groupby(group_cols)[target_col].shift(lag)
        else:
            out[f"aqi_lag_{lag}"] = out[target_col].shift(lag)
    return out


def add_rolling_features(df: pd.DataFrame, group_cols: list[str], target_col: str = "aqi_value") -> pd.DataFrame:
    out = df.copy()
    sort_columns = [col for col in group_cols + ["date"] if col in out.columns]
    if sort_columns:
        out = out.sort_values(sort_columns).reset_index(drop=True)
    else:
        out = out.reset_index(drop=True)
    for window in [3, 7, 14]:
        if all(col in out.columns for col in group_cols):
            out[f"aqi_rolling_mean_{window}"] = out.groupby(group_cols)[target_col].transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
            out[f"aqi_rolling_std_{window}"] = out.groupby(group_cols)[target_col].transform(lambda s: s.shift(1).rolling(window, min_periods=1).std())
        else:
            out[f"aqi_rolling_mean_{window}"] = out[target_col].shift(1).rolling(window, min_periods=1).mean()
            out[f"aqi_rolling_std_{window}"] = out[target_col].shift(1).rolling(window, min_periods=1).std()
    if all(col in out.columns for col in group_cols):
        out["aqi_change_1d"] = out.groupby(group_cols)[target_col].diff(1)
        out["aqi_change_3d"] = out.groupby(group_cols)[target_col].diff(3)
        out["aqi_trend_3d"] = out.groupby(group_cols)[target_col].transform(lambda s: s.shift(1).rolling(3, min_periods=1).mean().diff())
        out["aqi_trend_7d"] = out.groupby(group_cols)[target_col].transform(lambda s: s.shift(1).rolling(7, min_periods=1).mean().diff())
    else:
        out["aqi_change_1d"] = out[target_col].diff(1)
        out["aqi_change_3d"] = out[target_col].diff(3)
        out["aqi_trend_3d"] = out[target_col].shift(1).rolling(3, min_periods=1).mean().diff()
        out["aqi_trend_7d"] = out[target_col].shift(1).rolling(7, min_periods=1).mean().diff()
    return out


def create_targets(df: pd.DataFrame, horizon: int, group_cols: list[str], target_col: str = "aqi_value") -> pd.DataFrame:
    out = df.copy()
    sort_columns = [col for col in group_cols + ["date"] if col in out.columns]
    if sort_columns:
        out = out.sort_values(sort_columns).reset_index(drop=True)
    else:
        out = out.reset_index(drop=True)
    horizon_key = horizon if horizon in {24, 48, 72} else 24 if horizon == 1 else horizon
    target_name = f"target_aqi_{horizon_key}h"
    shifted = out.groupby(group_cols)[target_col].shift(-horizon) if all(col in out.columns for col in group_cols) else out[target_col].shift(-horizon)
    target_values = [None if value is None or (isinstance(value, float) and pd.isna(value)) else value for value in shifted.tolist()]
    out = out.copy()
    out[target_name] = pd.Series(target_values, dtype=object)
    if horizon_key != horizon and horizon in {1, 2, 3}:
        out[target_name] = shifted
    return out


def add_weather_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "temperature_celsius" in out.columns and "humidity" in out.columns:
        out["temperature_humidity_interaction"] = out["temperature_celsius"] * out["humidity"]
    if "wind_kph" in out.columns:
        out["wind_dispersion_score"] = out["wind_kph"] / (out["humidity"].clip(lower=1) if "humidity" in out.columns else 1)
    if "precip_mm" in out.columns:
        out["rain_cleaning_effect"] = out["precip_mm"] * -1
    if "temperature_celsius" in out.columns and "humidity" in out.columns:
        out["stagnation_index"] = out["humidity"] / (out["temperature_celsius"].clip(lower=1))
    if "visibility_km" in out.columns and "aqi_value" in out.columns:
        out["visibility_pollution_interaction"] = out["visibility_km"] / out["aqi_value"].clip(lower=1)
    return out


def add_pollutant_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    pollutant_columns = [c for c in ["pm2_5", "pm10", "no2", "so2", "co", "o3"] if c in out.columns]
    if "pm2_5" in out.columns and "pm10" in out.columns:
        out["pm_ratio"] = out["pm2_5"] / out["pm10"].replace(0, pd.NA)
        out["pm_ratio"] = out["pm_ratio"].fillna(0)
    if "pm2_5" in out.columns and "pm10" in out.columns:
        out["particulate_load"] = out["pm2_5"] + out["pm10"]
    if pollutant_columns:
        out["gas_pollution_index"] = out[pollutant_columns].mean(axis=1)
    out["dominant_measured_pollutant"] = ""
    return out


def add_monitoring_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    station_count = out.get("station_count")
    if station_count is None:
        out["station_count"] = 1
    else:
        out["station_count"] = station_count.fillna(1)
    out["station_reliability_score"] = out["station_count"] / (out["station_count"].max() if out["station_count"].max() > 0 else 1)
    return out
