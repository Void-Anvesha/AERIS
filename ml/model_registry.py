from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ml.config import METADATA_DIR, MODEL_VERSION
from ml.utils import save_json


def write_registry(results: dict[str, Any], feature_columns: list[str], training_rows: int, validation_rows: int, test_rows: int) -> dict[str, Any]:
    registry = {
        "project": "AERIS",
        "model_version": MODEL_VERSION,
        "status": "active",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "training_rows": training_rows,
        "validation_rows": validation_rows,
        "test_rows": test_rows,
        "feature_count": len(feature_columns),
        "features": feature_columns,
        "models": {},
    }
    for horizon, value in results.items():
        registry["models"][str(horizon)] = {
            "algorithm": value["best_model_name"],
            "metrics": value["results"][value["best_model_name"]]["metrics"],
        }
    save_json(METADATA_DIR / "model_registry.json", registry)
    return registry
