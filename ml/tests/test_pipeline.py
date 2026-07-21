import json
import pandas as pd
import pytest

from ml.data_cleaning import clean_aqi_data, clean_weather_data, validate_aqi_series
from ml.feature_engineering import add_lag_features, add_rolling_features, create_targets, add_time_features
from ml.location_matching import normalize_location, match_locations
from ml.train import chronological_split, predict_with_models, aqi_category, clip_predictions
from ml.predict import build_prediction_payload
from ml.utils import parse_date


def test_parse_date():
    parsed = parse_date("2024-01-15")
    assert parsed is not None


def test_aqi_validation():
    s = pd.Series([10, 120, 600, None], name="aqi_value")
    cleaned = validate_aqi_series(s)
    assert cleaned.notna().sum() == 2
    assert cleaned.iloc[0] == 10
    assert cleaned.iloc[1] == 120


def test_lag_generation():
    df = pd.DataFrame({"state": ["Delhi", "Delhi", "Delhi", "Delhi"], "area": ["A", "A", "A", "A"], "date": pd.date_range("2024-01-01", periods=4, freq="D"), "aqi_value": [100, 120, 130, 150]})
    out = add_lag_features(df, group_cols=["state", "area"], target_col="aqi_value")
    assert "aqi_lag_1" in out.columns
    assert out.loc[1, "aqi_lag_1"] == 100
    assert out.loc[2, "aqi_lag_1"] == 120


def test_rolling_mean_leakage():
    df = pd.DataFrame({"state": ["Delhi", "Delhi", "Delhi", "Delhi"], "area": ["A", "A", "A", "A"], "date": pd.date_range("2024-01-01", periods=4, freq="D"), "aqi_value": [100, 120, 130, 150]})
    out = add_rolling_features(df, group_cols=["state", "area"], target_col="aqi_value")
    assert "aqi_rolling_mean_3" in out.columns
    assert out.loc[2, "aqi_rolling_mean_3"] == 110.0


def test_location_matching():
    assert normalize_location("Bengaluru") == "bengaluru"
    matched = match_locations(["Bengaluru", "Bombay", "Gurgaon"], ["Bangalore", "Mumbai", "Gurugram"])
    assert matched[0]["match"] == "Bangalore"
    assert matched[1]["match"] == "Mumbai"
    assert matched[2]["match"] == "Gurugram"


def test_chronological_split():
    df = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=20, freq="D"), "aqi_value": list(range(20))})
    train, val, test = chronological_split(df, train_ratio=0.7, val_ratio=0.15)
    assert len(train) > 0 and len(val) > 0 and len(test) > 0
    assert train["date"].max() < val["date"].min()
    assert val["date"].max() < test["date"].min()


def test_target_generation():
    df = pd.DataFrame({"state": ["Delhi"] * 5, "area": ["A"] * 5, "date": pd.date_range("2024-01-01", periods=5, freq="D"), "aqi_value": [100, 110, 120, 130, 140]})
    out = create_targets(df, horizon=1, group_cols=["state", "area"], target_col="aqi_value")
    assert "target_aqi_24h" in out.columns
    assert pd.isna(out.iloc[-1]["target_aqi_24h"])


def test_time_features_use_unique_season_labels():
    df = pd.DataFrame({"state": ["Delhi"] * 4, "area": ["A"] * 4, "date": pd.date_range("2024-01-01", periods=4, freq="D"), "aqi_value": [100, 110, 120, 130]})
    out = add_time_features(df)
    assert set(out["season"].dropna().unique()) <= {"Winter", "Summer", "Monsoon", "Post-Monsoon"}


def test_model_loading(tmp_path):
    import joblib
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(random_state=0)
    model.fit([[0], [1]], [0, 1])
    joblib.dump(model, tmp_path / "model.joblib")
    loaded = joblib.load(tmp_path / "model.joblib")
    assert loaded.predict([[2]])[0] >= 0


def test_prediction_range():
    preds = clip_predictions([600, -10, 120])
    assert preds[0] == 500
    assert preds[1] == 0
    assert preds[2] == 120


def test_aqi_category_conversion():
    assert aqi_category(20) == "Good"
    assert aqi_category(120) == "Moderate"
    assert aqi_category(450) == "Severe"


def test_missing_location():
    payload = build_prediction_payload(state="Unknown", area="Missing", history=[])
    assert payload["success"] is False
    assert payload["status"] == "insufficient_data"


def test_insufficient_history():
    payload = build_prediction_payload(state="Delhi", area="Anand Vihar", history=[{"aqi_value": 100}])
    assert payload["success"] is False
    assert payload["status"] == "insufficient_data"


def test_confidence_range():
    result = predict_with_models(pd.DataFrame({"aqi_value": [100, 105, 110]}), horizon=24)
    assert 0 <= result["model_confidence"] <= 1


def test_api_response_schema():
    payload = build_prediction_payload(state="Delhi", area="Anand Vihar", history=[{"aqi_value": 100}, {"aqi_value": 110}, {"aqi_value": 120}, {"aqi_value": 130}, {"aqi_value": 140}])
    assert payload["location"]["state"] == "Delhi"
    assert isinstance(payload["forecast"], list)
