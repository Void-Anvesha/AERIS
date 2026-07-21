from __future__ import annotations

import pandas as pd

from app.services.data_pipeline.agents.data_fusion_agent import DataFusionAgent
from app.services.data_pipeline.agents.feature_engineering_agent import FeatureEngineeringAgent
from app.services.data_pipeline.repositories.processed_dataset_repository import ProcessedDatasetRepository


class DataPipeline:
    """Reusable orchestration layer for the data ingestion and feature pipeline."""

    def __init__(self) -> None:
        self.fusion_agent = DataFusionAgent()
        self.feature_agent = FeatureEngineeringAgent()
        self.repository = ProcessedDatasetRepository()

    def run(self, aqi_df: pd.DataFrame, weather_df: pd.DataFrame, traffic_df: pd.DataFrame) -> pd.DataFrame:
        fused_df = self.fusion_agent.run(aqi_df, weather_df, traffic_df)
        engineered_df = self.feature_agent.run(fused_df)
        self.repository.save(engineered_df)
        return engineered_df
