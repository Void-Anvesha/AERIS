"""Hotspot & Event Detection Agent module for identifying environmental pollution spikes and causes."""

from typing import Dict, Any, Union, List, Optional
from pydantic import BaseModel, Field

from app.core.exceptions import ValidationError, AERISException
from app.core.logging import logger
from app.services.geospatial.geo_utils import validate_coordinates
from app.services.hotspot.timeline import TimelineAnalyzer
from app.services.hotspot.cluster_detector import ClusterDetector
from app.services.hotspot.event_detector import EventDetector
from app.services.hotspot.severity import SeverityCalculator


class HotspotInput(BaseModel):
    """Pydantic model for input data to the Hotspot Agent."""
    latitude: float = Field(..., description="Target latitude coordinate (-90 to 90)")
    longitude: float = Field(..., description="Target longitude coordinate (-180 to 180)")
    aqi: float = Field(..., ge=0.0, description="Current Air Quality Index reading")
    pm25: float = Field(..., ge=0.0, description="PM2.5 concentration (ug/m3)")
    pm10: float = Field(..., ge=0.0, description="PM10 concentration (ug/m3)")
    weather: Dict[str, Any] = Field(default_factory=dict, description="Current & forecast weather indicators")
    history: List[Dict[str, Any]] = Field(default_factory=list, description="Historical timeline readings")
    nearby_objects: List[Dict[str, Any]] = Field(default_factory=list, description="Enriched nearby infrastructure objects")


class HotspotOutput(BaseModel):
    """Pydantic model for output response from the Hotspot Agent."""
    hotspot: bool = Field(..., description="Boolean flag indicating whether location is a pollution hotspot")
    cluster: str = Field(..., description="DBSCAN cluster designation (e.g. Cluster-A)")
    severity: int = Field(..., ge=0, le=100, description="Hotspot severity score normalized between 0 and 100")
    cause: str = Field(..., description="Inferred root cause of pollution spike")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Inference confidence score between 0.0 and 1.0")
    recommendation: str = Field(..., description="Actionable environmental intervention recommendation")


class HotspotAgent:
    """Hotspot Agent for detecting pollution clusters, events, root causes, and severity scores."""

    def __init__(self) -> None:
        """Initialize HotspotAgent instance and component detectors."""
        logger.info("Initializing HotspotAgent instance.")
        self.timeline_analyzer = TimelineAnalyzer()
        self.cluster_detector = ClusterDetector()
        self.event_detector = EventDetector()
        self.severity_calculator = SeverityCalculator()

    def analyze_hotspot(self, input_data: Union[Dict[str, Any], HotspotInput]) -> Dict[str, Any]:
        """Perform end-to-end hotspot and event detection on enriched geospatial input.

        Pipeline Steps:
        1. Validate coordinates & schema.
        2. Detect AQI spikes via timeline history analysis.
        3. Cluster spatial coordinates using DBSCAN algorithm.
        4. Infer root pollution causes using rule-based reasoning engine.
        5. Compute normalized severity score (0-100).
        6. Generate actionable intervention recommendation.
        7. Return structured dictionary output matching output schema requirements.

        Args:
            input_data: Dictionary or HotspotInput instance containing geospatial and AQI metrics.

        Returns:
            Dict containing hotspot boolean, cluster label, severity score, cause, confidence, recommendation.

        Raises:
            ValidationError: If input validation fails.
            AERISException: If processing fails during pipeline execution.
        """
        logger.info("Starting analyze_hotspot execution.")

        try:
            # Step 1: Input schema validation
            if isinstance(input_data, dict):
                try:
                    parsed_input = HotspotInput(**input_data)
                except Exception as ve:
                    logger.error(f"Hotspot input schema validation error: {str(ve)}")
                    raise ValidationError(f"Invalid hotspot input schema: {str(ve)}")
            elif isinstance(input_data, HotspotInput):
                parsed_input = input_data
            else:
                raise ValidationError("Input must be a dictionary or HotspotInput instance.")

            # Validate coordinate bounds
            validate_coordinates(parsed_input.latitude, parsed_input.longitude)

            # Step 2: Detect AQI spikes and historical timeline trend
            timeline_info = self.timeline_analyzer.analyze_history(
                current_aqi=parsed_input.aqi,
                current_pm25=parsed_input.pm25,
                current_pm10=parsed_input.pm10,
                history=parsed_input.history
            )

            # Step 3: Cluster nearby coordinates using DBSCAN
            cluster_info = self.cluster_detector.detect_cluster(
                target_lat=parsed_input.latitude,
                target_lon=parsed_input.longitude,
                nearby_objects=parsed_input.nearby_objects
            )

            # Step 4: Detect possible pollution cause & confidence
            cause, confidence = self.event_detector.detect_cause(
                aqi=parsed_input.aqi,
                pm25=parsed_input.pm25,
                pm10=parsed_input.pm10,
                weather=parsed_input.weather,
                nearby_objects=parsed_input.nearby_objects,
                timeline_info=timeline_info
            )

            # Extract population density string if present in nearby_objects or default
            pop_density_str = "High Density Urban"
            for obj in parsed_input.nearby_objects:
                if "population_density" in obj:
                    pop_density_str = str(obj["population_density"])
                    break

            # Step 5 & 6: Generate severity score (0-100) & recommendation
            severity_score, recommendation = self.severity_calculator.calculate_severity(
                aqi=parsed_input.aqi,
                population_density_str=pop_density_str,
                nearby_objects=parsed_input.nearby_objects,
                weather=parsed_input.weather,
                timeline_info=timeline_info,
                cause=cause
            )

            # Determine hotspot status boolean
            is_hotspot = (
                parsed_input.aqi >= 150.0 or
                timeline_info.get("is_spike", False) or
                severity_score >= 60 or
                cluster_info.get("is_clustered", False)
            )

            # Step 7: Construct & validate output model
            output_model = HotspotOutput(
                hotspot=is_hotspot,
                cluster=cluster_info["cluster"],
                severity=severity_score,
                cause=cause,
                confidence=round(confidence, 2),
                recommendation=recommendation
            )

            logger.info(
                f"Hotspot analysis completed successfully: hotspot={is_hotspot}, "
                f"cluster={cluster_info['cluster']}, severity={severity_score}, cause='{cause}'"
            )
            return output_model.model_dump()

        except ValidationError:
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during hotspot analysis: {str(e)}")
            raise AERISException(f"Hotspot analysis failed: {str(e)}")

    def analyze(self, input_data: Union[Dict[str, Any], HotspotInput]) -> Dict[str, Any]:
        """Alias for analyze_hotspot method."""
        return self.analyze_hotspot(input_data)
