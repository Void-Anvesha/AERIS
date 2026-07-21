from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from ml.config import RAW_DATA_DIR, REPORTS_DIR
from ml.data_loader import discover_data_files, load_csv_or_excel
from ml.utils import save_json


def inspect_data(root: str | Path | None = None) -> dict[str, Any]:
    files = discover_data_files(root or RAW_DATA_DIR)
    report = {"files": []}
    if not files:
        report["message"] = "No AQI or weather files were found in the data/raw directory."
    for file_path in files:
        sheets = load_csv_or_excel(file_path)
        for sheet_name, frame in sheets.items():
            frame = frame.copy()
            report["files"].append({
                "file": str(file_path),
                "sheet": sheet_name,
                "rows": int(len(frame)),
                "columns": list(frame.columns),
                "dtypes": {column: str(dtype) for column, dtype in frame.dtypes.items()},
                "missing_percentage": {column: round(float(frame[column].isna().mean() * 100), 2) for column in frame.columns},
                "duplicates": int(frame.duplicated().sum()),
                "date_range": {},
                "unique_states": [],
                "unique_areas": [],
            })
            for column in frame.columns:
                if column.lower() in {"date", "datetime", "timestamp", "last_updated"}:
                    parsed = pd.to_datetime(frame[column], errors="coerce")
                    if parsed.notna().any():
                        report["files"][-1]["date_range"] = {
                            "min": parsed.min().date().isoformat() if pd.notna(parsed.min()) else None,
                            "max": parsed.max().date().isoformat() if pd.notna(parsed.max()) else None,
                        }
            for column in ["state", "region", "location_name", "area"]:
                if column in frame.columns:
                    report["files"][-1]["unique_states"] = list(frame[column].dropna().astype(str).unique()[:20])
                    break
            for column in ["area", "location_name", "location"]:
                if column in frame.columns:
                    report["files"][-1]["unique_areas"] = list(frame[column].dropna().astype(str).unique()[:20])
                    break
    save_json(REPORTS_DIR / "data_quality.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect AQI and weather data files.")
    parser.add_argument("--root", default=str(RAW_DATA_DIR))
    args = parser.parse_args()
    inspect_data(args.root)


if __name__ == "__main__":
    main()
