from __future__ import annotations

from typing import Any

import pandas as pd
from sqlalchemy import text

from app.db.session import SessionLocal


class ProcessedDatasetRepository:
    """Persist processed data into PostgreSQL using SQLAlchemy."""

    def save(self, dataset: pd.DataFrame) -> None:
        with SessionLocal() as session:
            session.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS processed_air_quality (
                        date TIMESTAMP,
                        city VARCHAR(100),
                        aqi DOUBLE PRECISION,
                        temperature DOUBLE PRECISION,
                        humidity DOUBLE PRECISION,
                        traffic_index DOUBLE PRECISION,
                        industrial_score DOUBLE PRECISION,
                        green_cover DOUBLE PRECISION,
                        season VARCHAR(50),
                        weekend INTEGER,
                        lag_aqi DOUBLE PRECISION,
                        rolling_mean_aqi DOUBLE PRECISION,
                        health_risk VARCHAR(50)
                    )
                    """
                )
            )
            for _, row in dataset.iterrows():
                session.execute(
                    text(
                        """
                        INSERT INTO processed_air_quality (date, city, aqi, temperature, humidity, traffic_index, industrial_score, green_cover, season, weekend, lag_aqi, rolling_mean_aqi, health_risk)
                        VALUES (:date, :city, :aqi, :temperature, :humidity, :traffic_index, :industrial_score, :green_cover, :season, :weekend, :lag_aqi, :rolling_mean_aqi, :health_risk)
                        ON CONFLICT DO NOTHING
                        """
                    ),
                    {
                        "date": row["date"],
                        "city": row["city"],
                        "aqi": float(row.get("aqi", 0)),
                        "temperature": float(row.get("temperature", 0)),
                        "humidity": float(row.get("humidity", 0)),
                        "traffic_index": float(row.get("traffic_index", 0)),
                        "industrial_score": float(row.get("industrial_score", 0)),
                        "green_cover": float(row.get("green_cover", 0)),
                        "season": row.get("season", "Unknown"),
                        "weekend": int(row.get("weekend", 0)),
                        "lag_aqi": float(row.get("lag_aqi", 0)),
                        "rolling_mean_aqi": float(row.get("rolling_mean_aqi", 0)),
                        "health_risk": row.get("health_risk", "Low"),
                    },
                )
            session.commit()
