# AERIS

AERIS is an AI-powered Urban Air Quality Intelligence Platform for smart cities.

## AQI Forecasting Module

The repository now includes a production-oriented AQI forecasting pipeline that inspects available data, performs cleaning and feature engineering, trains multiple regressors, evaluates them, saves artifacts, and exposes forecasting APIs through FastAPI.

### Data locations
- Place AQI and weather files under [data/raw](data/raw) or update the loader paths in [ml/data_loader.py](ml/data_loader.py).
- Expected AQI columns include date, state, area, aqi_value, prominent_pollutants, air_quality_status.
- Expected weather columns include date, state, location_name, temperature_celsius, humidity, wind_kph, pressure_mb, precip_mm, cloud, visibility_km, pm2_5, pm10, no2, so2, co, o3.

### Pipeline overview
1. Inspect data with [ml/inspect_data.py](ml/inspect_data.py).
2. Merge AQI and weather data with [ml/merge_datasets.py](ml/merge_datasets.py).
3. Engineer time, lag, rolling, weather, pollutant, and monitoring features with [ml/feature_engineering.py](ml/feature_engineering.py).
4. Train horizons 24h, 48h, and 72h using [ml/train.py](ml/train.py).
5. Generate explanations and save artifacts under [ml/artifacts](ml/artifacts).

### Commands
- python -m ml.inspect_data
- python -m ml.merge_datasets
- python -m ml.train --demo-mode --max-rows 50000
- python -m ml.evaluate
- python -m ml.predict --state "Delhi" --area "Anand Vihar"
- python -m ml.train --full-pipeline

### API endpoints
- GET /api/model/status
- GET /api/model/metrics
- GET /api/model/features
- GET /api/model/training-runs
- POST /api/model/train
- POST /api/forecast
- GET /api/forecast/{state}/{area}
- GET /api/model/train/status/{job_id}

### Notes
- Synthetic placeholders are not used for the final model outputs; the implementation uses real execution paths and saves actual metrics when data is available.
- If the dataset is missing or insufficient, the predictor returns a safe fallback with requires_human_review set to true.
