from __future__ import annotations

import pandas as pd


class FeatureEngineeringAgent:
    """Generate derived features for downstream analytics and modeling."""

    def run(self, processed_df: pd.DataFrame) -> pd.DataFrame:
        features_df = processed_df.copy()
        features_df = self._ensure_numerics(features_df)
        features_df = self._add_temporal_features(features_df)
        features_df = self._add_context_features(features_df)
        features_df = self._add_health_risk(features_df)
        return features_df

    def _ensure_numerics(self, df: pd.DataFrame) -> pd.DataFrame:
        for column in ["aqi", "temperature", "humidity", "traffic_index", "industrial_score", "green_cover"]:
            df[column] = pd.to_numeric(df.get(column, 0), errors="coerce").fillna(0.0)
        return df

    def _add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values(["city", "date"]).reset_index(drop=True)
        df["season"] = df["date"].dt.month.map(self._season_for_month)
        df["weekend"] = df["date"].dt.dayofweek.isin([5, 6]).astype(int)
        df["lag_aqi"] = df.groupby("city")["aqi"].shift(1)
        df["rolling_mean_aqi"] = df.groupby("city")["aqi"].transform(lambda s: s.rolling(3, min_periods=1).mean())
        return df

    def _add_context_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df["traffic_index"] = df.get("traffic_index", 0.0).fillna(0.0)
        df["industrial_score"] = df.get("industrial_score", 0.0).fillna(0.0)
        df["green_cover"] = df.get("green_cover", 0.0).fillna(0.0)
        return df

    def _add_health_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        df["health_risk"] = df["aqi"].apply(self._map_health_risk)
        return df

    @staticmethod
    def _season_for_month(month: int) -> str:
        return {
            12: "Winter",
            1: "Winter",
            2: "Winter",
            3: "Spring",
            4: "Spring",
            5: "Spring",
            6: "Summer",
            7: "Summer",
            8: "Summer",
            9: "Autumn",
            10: "Autumn",
            11: "Autumn",
        }.get(month, "Unknown")

    @staticmethod
    def _map_health_risk(aqi_value: float) -> str:
        if aqi_value >= 150:
            return "High"
        if aqi_value >= 100:
            return "Moderate"
        return "Low"
