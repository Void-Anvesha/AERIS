from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ML_DIR = ROOT_DIR / "ml"
ARTIFACTS_DIR = ML_DIR / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
PREPROCESSORS_DIR = ARTIFACTS_DIR / "preprocessors"
METADATA_DIR = ARTIFACTS_DIR / "metadata"
EXPLAINABILITY_DIR = ARTIFACTS_DIR / "explainability"
REPORTS_DIR = ML_DIR / "reports"

MODEL_VERSION = "aeris-aqi-v1"
TARGET_COLUMNS = ["target_aqi_24h", "target_aqi_48h", "target_aqi_72h"]
HORIZONS = {24: "24h", 48: "48h", 72: "72h"}

for directory in [RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, PREPROCESSORS_DIR, METADATA_DIR, EXPLAINABILITY_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
