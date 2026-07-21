"""
Schemas describing the raw air-quality "insight" payload that feeds the
Decision Intelligence Agent and API responses.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PopulationDensity(str, Enum):
    """Qualitative population-density buckets used by the rule engine."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class InsightInput(BaseModel):
    """Raw air-quality insight for a single monitored zone/hotspot.

    Attributes:
        aqi: Current measured Air Quality Index (0-500+ scale).
        forecast: Forecasted AQI for the next monitoring window.
        confidence: Model confidence for the forecast, in the range [0, 1].
        dominant_pollutant: The pollutant currently driving the AQI value.
        source: Suspected/attributed emission source (e.g. "Construction").
        hotspot: Whether this zone is flagged as a persistent pollution hotspot.
        nearby_schools: Count of schools within the affected radius.
        nearby_hospitals: Count of hospitals within the affected radius.
        population_density: Qualitative population density of the zone.
    """

    aqi: float = Field(..., ge=0, description="Current measured AQI")
    forecast: float = Field(..., ge=0, description="Forecasted AQI")
    confidence: float = Field(..., ge=0, le=1, description="Forecast confidence [0-1]")
    dominant_pollutant: str = Field(..., min_length=1, description="e.g. PM2.5, PM10, NO2, O3")
    source: str = Field(..., min_length=1, description="Attributed emission source")
    hotspot: bool = Field(default=False, description="Persistent pollution hotspot flag")
    nearby_schools: int = Field(default=0, ge=0, description="Schools within affected radius")
    nearby_hospitals: int = Field(default=0, ge=0, description="Hospitals within affected radius")
    population_density: PopulationDensity = Field(
        default=PopulationDensity.MEDIUM, description="Qualitative population density"
    )
    zone_name: Optional[str] = Field(default=None, description="Optional human-readable zone/ward name")

    @field_validator("dominant_pollutant", "source")
    @classmethod
    def _strip_and_title(cls, value: str) -> str:
        """Normalise free-text fields so downstream matching is reliable."""
        return value.strip()

    model_config = {
        "json_schema_extra": {
            "example": {
                "aqi": 312,
                "forecast": 340,
                "confidence": 0.92,
                "dominant_pollutant": "PM2.5",
                "source": "Construction",
                "hotspot": True,
                "nearby_schools": 4,
                "nearby_hospitals": 2,
                "population_density": "High",
            }
        }
    }


class InsightResponse(BaseModel):
    city: str
    current_aqi: int = Field(..., ge=0)
    status: str
    trend: str
    forecast_next_24h: int = Field(..., ge=0)
    forecast_next_72h: int = Field(..., ge=0)
    recommendation: str
    advisory: str
