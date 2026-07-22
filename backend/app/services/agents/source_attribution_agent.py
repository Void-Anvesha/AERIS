"""Source Attribution Agent module for computing pollution contributor breakdown."""

import logging
from typing import Dict, Any, List
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class SourceAttributionInput(BaseModel):
    aqi: float = Field(..., ge=0.0)
    pm25: float = Field(..., ge=0.0)
    pm10: float = Field(..., ge=0.0)
    weather: Dict[str, Any] = Field(default_factory=dict)
    nearby_objects: List[Dict[str, Any]] = Field(default_factory=list)

class SourceAttributionOutput(BaseModel):
    traffic: float = Field(..., description="Traffic emissions share (0 to 100)")
    construction: float = Field(..., description="Construction dust emissions share (0 to 100)")
    industry: float = Field(..., description="Industrial emissions share (0 to 100)")
    biomass: float = Field(..., description="Biomass and crop burning emissions share (0 to 100)")
    dust: float = Field(..., description="Road and windblown dust share (0 to 100)")
    confidence: float = Field(0.90, ge=0.0, le=1.0)

class SourceAttributionAgent:
    """Agent that determines WHY AQI increased, modeling contributor breakdown."""

    def __init__(self) -> None:
        logger.info("Initializing SourceAttributionAgent.")

    def attribute_sources(self, payload: SourceAttributionInput) -> Dict[str, Any]:
        """Compute percentage breakdown of pollution sources based on ratios and nearby assets."""
        logger.info("Executing source attribution analysis.")
        
        # Extract features
        pm25 = payload.pm25
        pm10 = payload.pm10
        nearby = [obj.get("category", "").lower() for obj in payload.nearby_objects]
        
        # Default baseline values
        traffic = 20.0
        construction = 20.0
        industry = 20.0
        biomass = 20.0
        dust = 20.0
        
        pm_ratio = pm10 / pm25 if pm25 > 0 else 1.0
        
        # Heavy vehicle influence
        if "roads" in nearby or "road" in nearby:
            traffic += 25.0
            dust += 5.0
            construction -= 15.0
            industry -= 15.0
            
        # Construction influence (Coarse dust PM10)
        if "construction sites" in nearby or "construction site" in nearby or pm_ratio >= 1.6:
            construction += 30.0
            dust += 10.0
            traffic -= 10.0
            industry -= 10.0
            biomass -= 20.0
            
        # Industrial influence
        if "industries" in nearby or "industrial" in nearby or "factory" in nearby:
            industry += 35.0
            traffic -= 10.0
            biomass -= 10.0
            dust -= 15.0

        # Weather factors (e.g. low humidity + dry weather -> crop/biomass burning)
        humidity = payload.weather.get("humidity", 50.0)
        if humidity < 40.0 and pm25 > 80.0:
            biomass += 25.0
            traffic -= 10.0
            dust -= 15.0
            
        # Re-normalize to exactly 100%
        total = traffic + construction + industry + biomass + dust
        if total > 0:
            traffic = round((traffic / total) * 100.0, 1)
            construction = round((construction / total) * 100.0, 1)
            industry = round((industry / total) * 100.0, 1)
            biomass = round((biomass / total) * 100.0, 1)
            dust = round(100.0 - (traffic + construction + industry + biomass), 1) # Close remainder
            
        output = SourceAttributionOutput(
            traffic=max(0.0, traffic),
            construction=max(0.0, construction),
            industry=max(0.0, industry),
            biomass=max(0.0, biomass),
            dust=max(0.0, dust),
            confidence=0.92
        )
        return output.model_dump()
