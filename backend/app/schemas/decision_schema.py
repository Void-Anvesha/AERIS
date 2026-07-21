"""
Schemas describing the output of the Decision Intelligence Agent, which
also doubles as the input contract for the LLM Advisory Agent.
"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Priority levels assigned by the Decision Intelligence Agent."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class DecisionOutput(BaseModel):
    """Structured decision produced by the Decision Intelligence Agent.

    This is the canonical contract between Agent 1 (Decision Intelligence)
    and Agent 2 (LLM Advisory), and is also returned directly by the
    `POST /decision` endpoint.
    """

    risk_score: int = Field(..., ge=0, le=100, description="Composite risk score (0-100)")
    priority: Priority = Field(..., description="Overall priority classification")
    authority: str = Field(..., description="Responsible authority to be notified")
    response_time: str = Field(..., description="Expected/mandated response SLA")
    recommended_actions: List[str] = Field(
        default_factory=list, description="Concrete, ordered action items for the authority"
    )
    reason: List[str] = Field(
        default_factory=list, description="Human-readable justification for the score/priority"
    )
    manual_review_required: bool = Field(
        default=False, description="True when forecast confidence is below the trust threshold"
    )

    # Echoed context - useful for the LLM Advisory Agent and for audit/logging,
    # without forcing every downstream consumer to re-fetch the original insight.
    aqi: Optional[float] = Field(default=None, description="Echoed current AQI")
    forecast: Optional[float] = Field(default=None, description="Echoed forecasted AQI")
    dominant_pollutant: Optional[str] = Field(default=None, description="Echoed dominant pollutant")
    source: Optional[str] = Field(default=None, description="Echoed attributed source")
    zone_name: Optional[str] = Field(default=None, description="Echoed zone/ward name, if provided")

    model_config = {
        "json_schema_extra": {
            "example": {
                "risk_score": 96,
                "priority": "Critical",
                "authority": "Municipal Corporation",
                "response_time": "Within 2 Hours",
                "recommended_actions": [
                    "Inspect construction sites for dust-control compliance",
                    "Deploy anti-smog guns and road sprinkling in the hotspot zone",
                    "Restrict heavy vehicle movement during peak hours",
                    "Increase AQI monitoring frequency to hourly",
                ],
                "reason": [
                    "Current AQI (312) falls in the Critical band (>300)",
                    "Forecast AQI (340) is higher than current AQI, indicating a worsening trend",
                    "Zone flagged as a persistent pollution hotspot",
                    "4 schools located within the affected radius",
                    "2 hospitals located within the affected radius",
                    "High population density increases exposure risk",
                ],
                "manual_review_required": False,
                "aqi": 312,
                "forecast": 340,
                "dominant_pollutant": "PM2.5",
                "source": "Construction",
                "zone_name": None,
            }
        }
    }
