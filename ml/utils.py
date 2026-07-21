from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import pandas as pd

from ml.config import ROOT_DIR


def ensure_directory(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(path: str | Path, payload: dict[str, Any]) -> Path:
    path = ensure_directory(path if not isinstance(path, (str, Path)) else Path(path)) if not isinstance(path, (str, Path)) else Path(path)
    if path.suffix != ".json":
        path = path.with_suffix(".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, default=str)
    return path


def load_json(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_date(value: Any) -> pd.Timestamp | pd.NaT:
    if pd.isna(value):
        return pd.NaT
    if isinstance(value, pd.Timestamp):
        return value
    if isinstance(value, str):
        text = value.strip()
        for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"]:
            try:
                return pd.to_datetime(text, format=fmt)
            except ValueError:
                continue
    try:
        return pd.to_datetime(value)
    except (TypeError, ValueError):
        return pd.NaT


def normalize_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def clip_predictions(values: list[float] | pd.Series | pd.Index) -> list[float]:
    series = pd.Series(values)
    return [float(max(0.0, min(500.0, float(v)))) for v in series]
