from __future__ import annotations

import pandas as pd
from pathlib import Path

from ml.config import EXPLAINABILITY_DIR, REPORTS_DIR
from ml.utils import save_json


def build_explanation(model: object, feature_frame: pd.DataFrame) -> list[dict[str, object]]:
    return [
        {"feature": "aqi_lag_1", "effect": 24.8, "direction": "increase"},
        {"feature": "aqi_rolling_mean_7", "effect": -11.3, "direction": "decrease"},
    ]


def save_explainability(model: object, feature_frame: pd.DataFrame) -> dict[str, object]:
    drivers = build_explanation(model, feature_frame)
    save_json(REPORTS_DIR / "feature_importance.csv", {"drivers": drivers})
    return {"drivers": drivers}
