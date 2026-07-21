from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from ml.config import MODEL_VERSION
from ml.train import aqi_category, predict_with_models


def _validate_prediction_input(state: str, area: str, history: list[dict[str, Any]] | None) -> tuple[bool, str | None]:
    if not state or not area:
        return False, "Missing location"
    if not history or len(history) < 5:
        return False, "Insufficient history"
    latest_aqi = None
    for item in history:
        if isinstance(item, dict) and item.get("aqi_value") is not None:
            latest_aqi = item.get("aqi_value")
    if latest_aqi is None:
        return False, "Missing AQI history"
    return True, None


def build_prediction_payload(state: str, area: str, history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    valid, error = _validate_prediction_input(state, area, history)
    if not valid:
        return {"success": False, "status": "insufficient_data", "message": "There is not enough reliable historical data to generate this forecast.", "requires_human_review": True, "location": {"state": state, "area": area}, "forecast": []}
    records = []
    for item in history:
        if isinstance(item, dict):
            records.append({"state": state, "area": area, "date": item.get("date", pd.Timestamp.utcnow()), "aqi_value": item.get("aqi_value", 0)})
    frame = pd.DataFrame(records)
    if "date" in frame.columns:
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame = frame.sort_values("date").reset_index(drop=True)
    current_aqi = float(frame["aqi_value"].iloc[-1])
    forecast = []
    for horizon in [24, 48, 72]:
        prediction = predict_with_models(frame, horizon=horizon)
        forecast.append({
            "horizon_hours": horizon,
            "predicted_aqi": round(min(500, max(0, float(prediction["predicted_aqi"]))), 2),
            "category": aqi_category(float(prediction["predicted_aqi"])),
            "model_confidence": round(float(prediction["model_confidence"]), 2),
            "confidence_level": prediction["confidence_level"],
        })
    return {
        "success": True,
        "location": {"state": state, "area": area},
        "current_aqi": round(current_aqi, 2),
        "forecast": forecast,
        "model_version": MODEL_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AQI forecasts for a location.")
    parser.add_argument("--state", required=True)
    parser.add_argument("--area", required=True)
    args = parser.parse_args()
    payload = build_prediction_payload(args.state, args.area, [{"aqi_value": 120}, {"aqi_value": 130}, {"aqi_value": 125}, {"aqi_value": 140}, {"aqi_value": 150}])
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
