from pydantic import BaseModel, Field


class InsightResponse(BaseModel):
    city: str
    current_aqi: int = Field(..., ge=0)
    status: str
    trend: str
    forecast_next_24h: int = Field(..., ge=0)
    forecast_next_72h: int = Field(..., ge=0)
    recommendation: str
    advisory: str
