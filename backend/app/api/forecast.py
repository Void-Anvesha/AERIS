from threading import Lock
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ml.predict import build_prediction_payload
from ml.train import run_training

router = APIRouter(prefix="/api", tags=["forecast"])


class TrainRequest(BaseModel):
    demo_mode: bool = True
    max_rows: int | None = None
    retrain: bool = True


class ForecastRequest(BaseModel):
    state: str = Field(...)
    area: str = Field(...)
    history: list[dict[str, Any]] | None = None


class ForecastResponse(BaseModel):
    success: bool
    location: dict[str, str]
    current_aqi: float | None = None
    forecast: list[dict[str, Any]]
    model_version: str | None = None
    generated_at: str | None = None


training_jobs: dict[str, dict[str, Any]] = {}
training_lock = Lock()


@router.get("/model/status")
def get_model_status() -> dict[str, Any]:
    return {"status": "ready", "model_version": "aeris-aqi-v1"}


@router.get("/model/metrics")
def get_model_metrics() -> dict[str, Any]:
    return {"metrics": {"status": "not_trained_yet"}}


@router.get("/model/features")
def get_model_features() -> dict[str, Any]:
    return {"features": ["aqi_lag_1", "aqi_rolling_mean_7", "pm2_5", "wind_kph", "humidity", "precip_mm", "temperature_celsius"]}


@router.get("/model/training-runs")
def get_training_runs() -> list[dict[str, Any]]:
    return list(training_jobs.values())


@router.post("/model/train", status_code=status.HTTP_202_ACCEPTED)
def train_model(payload: TrainRequest) -> dict[str, Any]:
    active_jobs = [job for job in training_jobs.values() if job.get("status") not in {"completed", "failed"}]
    if active_jobs:
        raise HTTPException(status_code=409, detail="A training job is already in progress")
    with training_lock:
        job_id = f"job-{len(training_jobs) + 1}"
        training_jobs[job_id] = {"job_id": job_id, "status": "queued", "started_at": None, "completed_at": None, "error": None}
        try:
            training_jobs[job_id]["status"] = "loading_data"
            training_jobs[job_id]["started_at"] = None
            result = run_training(max_rows=payload.max_rows, demo_mode=payload.demo_mode, status_callback=lambda status: training_jobs[job_id].update(status=status))
            training_jobs[job_id]["status"] = "completed"
            training_jobs[job_id]["result"] = result
            training_jobs[job_id]["completed_at"] = None
            return {"job_id": job_id, "status": "completed", "result": result}
        except Exception as exc:  # pragma: no cover
            training_jobs[job_id]["status"] = "failed"
            training_jobs[job_id]["error"] = str(exc)
            raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/model/train/status/{job_id}")
def get_training_status(job_id: str) -> dict[str, Any]:
    job = training_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/forecast", response_model=ForecastResponse)
def forecast(payload: ForecastRequest) -> ForecastResponse:
    result = build_prediction_payload(payload.state, payload.area, payload.history)
    return ForecastResponse(**result)


@router.get("/forecast/{state}/{area}")
def get_forecast(state: str, area: str) -> dict[str, Any]:
    return build_prediction_payload(state, area, [{"aqi_value": 120}, {"aqi_value": 130}, {"aqi_value": 125}, {"aqi_value": 140}, {"aqi_value": 150}])
