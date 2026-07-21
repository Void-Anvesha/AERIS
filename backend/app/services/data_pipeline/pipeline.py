from __future__ import annotations

from typing import Any, Dict, List, Tuple, Callable

import pandas as pd

from app.services.data_pipeline.agents.data_fusion_agent import DataFusionAgent
from app.services.data_pipeline.agents.feature_engineering_agent import FeatureEngineeringAgent
from app.services.data_pipeline.repositories.processed_dataset_repository import ProcessedDatasetRepository
from app.services.orchestration.orchestrator import OrchestratorAgent


class DataPipeline:
    """Reusable orchestration layer for the data ingestion and feature pipeline."""

    def __init__(self) -> None:
        self.fusion_agent = DataFusionAgent()
        self.feature_agent = FeatureEngineeringAgent()
        self.repository = ProcessedDatasetRepository()
        self.orchestrator = OrchestratorAgent()

    def run(self, aqi_df: pd.DataFrame, weather_df: pd.DataFrame, traffic_df: pd.DataFrame) -> pd.DataFrame:
        fused_df: pd.DataFrame | None = None

        def fusion_task() -> Dict[str, Any]:
            nonlocal fused_df
            fused_df = self.fusion_agent.run(aqi_df, weather_df, traffic_df)
            return {"data": fused_df}

        def feature_task() -> Dict[str, Any]:
            if fused_df is None:
                raise RuntimeError("Fusion task did not produce data before feature engineering.")
            engineered = self.feature_agent.run(fused_df)
            return {"data": engineered}

        tasks: List[Tuple[str, Callable[[], Dict[str, Any]]]] = [
            ("DataFusionAgent", fusion_task),
            ("FeatureEngineeringAgent", feature_task),
        ]

        orchestrator_result = self.orchestrator.run(tasks)
        if orchestrator_result["status"] == "fallback":
            raise RuntimeError(
                f"Data pipeline failed at {orchestrator_result['failed_agent']}: {orchestrator_result['error']}"
            )

        engineered_df = orchestrator_result["last_known_good_state"]["data"]
        self.repository.save(engineered_df)
        return engineered_df
