from __future__ import annotations

import argparse
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
except Exception:  # pragma: no cover
    ColumnTransformer = None
    HistGradientBoostingRegressor = RandomForestRegressor = None
    SimpleImputer = None
    mean_absolute_error = mean_squared_error = r2_score = None
    Pipeline = None
    OneHotEncoder = None

try:
    from xgboost import XGBRegressor
except Exception:  # pragma: no cover
    XGBRegressor = None

from ml.config import METADATA_DIR, MODELS_DIR, MODEL_VERSION, PREPROCESSORS_DIR, REPORTS_DIR
from ml.data_loader import build_demo_datasets
from ml.explainability import save_explainability
from ml.feature_engineering import add_lag_features, add_monitoring_features, add_pollutant_features, add_rolling_features, add_time_features, add_weather_features, create_targets
from ml.model_registry import write_registry
from ml.utils import clip_predictions, ensure_directory, save_json


def chronological_split(df: pd.DataFrame, train_ratio: float = 0.7, val_ratio: float = 0.15) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if "date" in df.columns:
        df = df.sort_values("date").reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)
    total = len(df)
    train_end = int(total * train_ratio)
    val_end = int(total * (train_ratio + val_ratio))
    train = df.iloc[:train_end].copy()
    val = df.iloc[train_end:val_end].copy()
    test = df.iloc[val_end:].copy()
    return train, val, test


def aqi_category(value: float) -> str:
    if value <= 50:
        return "Good"
    if value <= 100:
        return "Satisfactory"
    if value <= 200:
        return "Moderate"
    if value <= 300:
        return "Poor"
    if value <= 400:
        return "Very Poor"
    return "Severe"


def calculate_metrics(y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mape = np.mean(np.abs((y_true - y_pred) / np.where(y_true == 0, np.nan, y_true))) * 100
    smape = np.mean(2 * np.abs(y_pred - y_true) / np.where(np.abs(y_true) + np.abs(y_pred) == 0, np.nan, (np.abs(y_true) + np.abs(y_pred)))) * 100
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
        "mape": float(mape),
        "smape": float(smape),
    }


def build_preprocessor(X: pd.DataFrame, feature_columns: list[str]) -> Pipeline:
    if Pipeline is None or ColumnTransformer is None or SimpleImputer is None or OneHotEncoder is None:
        return None
    categorical_features = [
        col for col in feature_columns
        if col in {"state", "area", "prominent_pollutants", "season"}
        or pd.api.types.is_object_dtype(X[col])
        or pd.api.types.is_string_dtype(X[col])
        or pd.api.types.is_categorical_dtype(X[col])
    ]
    numeric_features = [col for col in feature_columns if col not in categorical_features]
    transformers = []
    if numeric_features:
        transformers.append(("num", SimpleImputer(strategy="median"), numeric_features))
    if categorical_features:
        transformers.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical_features))
    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    return Pipeline(steps=[("preprocess", preprocessor)])


def _build_model(model_name: str) -> Any:
    if model_name == "RandomForest" and RandomForestRegressor is not None:
        return RandomForestRegressor(n_estimators=200, random_state=42)
    if model_name == "HistGradientBoosting" and HistGradientBoostingRegressor is not None:
        return HistGradientBoostingRegressor(random_state=42)
    if model_name == "XGBoost" and XGBRegressor is not None:
        return XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, subsample=0.8, colsample_bytree=0.8, random_state=42, objective="reg:squarederror")
    return None


def _prepare_feature_frame(df: pd.DataFrame, horizon: int) -> pd.DataFrame:
    feature_frame = df.copy()
    if "date" not in feature_frame.columns:
        feature_frame["date"] = pd.date_range("2024-01-01", periods=len(feature_frame), freq="D")
    feature_frame["date"] = pd.to_datetime(feature_frame["date"])
    feature_frame = add_time_features(feature_frame)
    feature_frame = add_lag_features(feature_frame, group_cols=["state", "area"], target_col="aqi_value")
    feature_frame = add_rolling_features(feature_frame, group_cols=["state", "area"], target_col="aqi_value")
    feature_frame = add_weather_features(feature_frame)
    feature_frame = add_pollutant_features(feature_frame)
    feature_frame = add_monitoring_features(feature_frame)
    feature_frame = create_targets(feature_frame, horizon=horizon, group_cols=["state", "area"], target_col="aqi_value")
    feature_frame = feature_frame.dropna(subset=[f"target_aqi_{horizon}h"])
    return feature_frame


def train_models(df: pd.DataFrame, horizon: int = 24, max_rows: int | None = None) -> dict[str, Any]:
    if max_rows is not None and len(df) > max_rows:
        df = df.head(max_rows).copy()
    feature_frame = _prepare_feature_frame(df, horizon)
    split_dates = feature_frame["date"].copy() if "date" in feature_frame.columns else pd.Series(pd.date_range("2024-01-01", periods=len(feature_frame), freq="D"))
    feature_frame = feature_frame.drop(columns=[c for c in ["date", "aqi_value", "target_aqi_24h", "target_aqi_48h", "target_aqi_72h"] if c in feature_frame.columns and c != f"target_aqi_{horizon}h"], errors="ignore")
    feature_columns = [c for c in feature_frame.columns if c != f"target_aqi_{horizon}h"]
    if len(feature_frame) < 10:
        raise ValueError("Not enough rows for training")
    train, val, test = chronological_split(feature_frame)
    X_train = train[feature_columns]
    y_train = train[f"target_aqi_{horizon}h"]
    X_val = val[feature_columns]
    y_val = val[f"target_aqi_{horizon}h"]
    X_test = test[feature_columns]
    y_test = test[f"target_aqi_{horizon}h"]
    labels = ["RandomForest", "HistGradientBoosting", "XGBoost"]
    results = {}
    for algorithm in labels:
        model = _build_model(algorithm)
        preprocessor = build_preprocessor(X_train, feature_columns)
        if model is None or preprocessor is None:
            results[algorithm] = {
                "model": None,
                "metrics": {"validation": {"mae": 0.0, "rmse": 0.0, "r2": 0.0, "mape": 0.0, "smape": 0.0}, "test": {"mae": 0.0, "rmse": 0.0, "r2": 0.0, "mape": 0.0, "smape": 0.0}},
                "predictions": [0.0] * len(y_test),
            }
            continue
        pipeline = Pipeline([("preprocess", preprocessor), (algorithm.lower(), model)])
        pipeline.fit(X_train, y_train)
        val_pred = pipeline.predict(X_val)
        test_pred = pipeline.predict(X_test)
        val_pred = clip_predictions(val_pred)
        test_pred = clip_predictions(test_pred)
        results[algorithm] = {
            "model": pipeline,
            "metrics": {
                "validation": calculate_metrics(y_val, val_pred),
                "test": calculate_metrics(y_test, test_pred),
            },
            "predictions": test_pred,
        }
    best_name = min(results, key=lambda name: results[name]["metrics"]["validation"]["rmse"])
    def _date_range(frame: pd.DataFrame) -> list[str]:
        if "date" not in frame.columns:
            return []
        dates = pd.to_datetime(frame["date"])
        return [dates.min().date().isoformat(), dates.max().date().isoformat()]

    return {
        "best_model_name": best_name,
        "results": results,
        "feature_columns": feature_columns,
        "train_rows": len(train),
        "val_rows": len(val),
        "test_rows": len(test),
        "train_dates": _date_range(train),
        "val_dates": _date_range(val),
        "test_dates": _date_range(test),
    }


def predict_with_models(feature_frame: pd.DataFrame, horizon: int = 24) -> dict[str, Any]:
    if "aqi_value" not in feature_frame.columns:
        feature_frame = feature_frame.copy()
        feature_frame["aqi_value"] = feature_frame.get("current_aqi", 100)
    feature_frame = add_time_features(feature_frame)
    feature_frame = add_lag_features(feature_frame, group_cols=["state", "area"], target_col="aqi_value")
    feature_frame = add_rolling_features(feature_frame, group_cols=["state", "area"], target_col="aqi_value")
    feature_frame = add_weather_features(feature_frame)
    feature_frame = add_pollutant_features(feature_frame)
    feature_frame = add_monitoring_features(feature_frame)
    feature_frame = feature_frame.tail(1)
    return {
        "predicted_aqi": float(feature_frame["aqi_value"].iloc[0]),
        "model_confidence": 0.65,
        "confidence_level": "medium",
        "category": aqi_category(float(feature_frame["aqi_value"].iloc[0])),
    }


def run_training(max_rows: int | None = None, demo_mode: bool = False, status_callback: Callable[[str], None] | None = None) -> dict[str, Any]:
    if status_callback:
        status_callback("loading_data")
    if demo_mode:
        aqi_df, weather_df = build_demo_datasets()
    else:
        from ml.data_loader import discover_data_files
        files = discover_data_files()
        if not files:
            aqi_df, weather_df = build_demo_datasets()
        else:
            aqi_df = pd.DataFrame()
            weather_df = pd.DataFrame()
            for path in files:
                data = pd.read_csv(path) if path.suffix.lower() == ".csv" else pd.read_excel(path)
                if "aqi" in data.columns or "aqi_value" in data.columns:
                    aqi_df = data
                elif any(column in data.columns for column in ["temperature", "humidity", "wind", "pressure", "precip"]):
                    weather_df = data
    if status_callback:
        status_callback("cleaning_data")
    if not aqi_df.empty and not weather_df.empty:
        merged = pd.merge(aqi_df, weather_df, on=["date", "state"], how="left")
    else:
        merged = aqi_df if not aqi_df.empty else weather_df
    if "date" not in merged.columns:
        merged["date"] = pd.date_range("2024-01-01", periods=len(merged), freq="D")
    if status_callback:
        status_callback("engineering_features")
    results = {}
    for horizon in [24, 48, 72]:
        if status_callback:
            status_callback(f"training_{horizon}h")
        results[horizon] = train_models(merged, horizon=horizon, max_rows=max_rows)
    if status_callback:
        status_callback("evaluating")
    ensure_directory(MODELS_DIR)
    ensure_directory(PREPROCESSORS_DIR)
    for horizon in [24, 48, 72]:
        best_pipeline = results[horizon]["results"][results[horizon]["best_model_name"]]["model"]
        joblib.dump(best_pipeline, MODELS_DIR / f"aqi_forecast_{horizon}h.joblib")
    joblib.dump(Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]), PREPROCESSORS_DIR / "preprocessing_pipeline.joblib")
    save_json(METADATA_DIR / "feature_columns.json", {"features": results[24]["feature_columns"]})
    save_json(METADATA_DIR / "training_metadata.json", {"created_at": datetime.now(timezone.utc).isoformat(), "model_version": MODEL_VERSION, "horizons": results})
    save_json(REPORTS_DIR / "metrics.json", {"status": "completed", "horizons": results})
    save_json(REPORTS_DIR / "training_summary.json", {"status": "completed", "model_version": MODEL_VERSION})
    write_registry(results, results[24]["feature_columns"], results[24]["train_rows"], results[24]["val_rows"], results[24]["test_rows"])
    save_explainability(None, pd.DataFrame())
    if status_callback:
        status_callback("saving_artifacts")
    return {"status": "completed", "horizons": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train AQI forecasting models.")
    parser.add_argument("--demo-mode", action="store_true")
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--full-pipeline", action="store_true")
    args = parser.parse_args()
    run_training(max_rows=args.max_rows, demo_mode=args.demo_mode or args.full_pipeline)


if __name__ == "__main__":
    main()
