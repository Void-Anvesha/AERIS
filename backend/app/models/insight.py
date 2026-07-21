from typing import List

from pydantic import BaseModel, Field


class Hotspot(BaseModel):
    name: str
    lat: float
    lng: float
    risk_level: str
    source: str


class SourceAttribution(BaseModel):
    traffic: float = Field(..., ge=0, le=1)
    industry: float = Field(..., ge=0, le=1)
    biomass: float = Field(..., ge=0, le=1)
    dust: float = Field(..., ge=0, le=1)


class IntelligenceSnapshot(BaseModel):
    city: str
    current_aqi: int
    status: str
    trend: str
    forecast_next_24h: int
    forecast_next_72h: int
    hotspots: List[Hotspot]
    source_attribution: SourceAttribution
    recommendation: str
    advisory: str
