"""Severity Calculator module for computing environmental hotspot severity scores and recommendations."""

from typing import Dict, Any, List, Tuple
from app.core.logging import logger


class SeverityCalculator:
    """Calculator for generating normalized severity scores (0-100) and actionable recommendations."""

    def __init__(self) -> None:
        """Initialize SeverityCalculator."""
        logger.info("Initializing SeverityCalculator service.")

    def calculate_severity(
        self,
        aqi: float,
        population_density_str: str,
        nearby_objects: List[Dict[str, Any]],
        weather: Dict[str, Any],
        timeline_info: Dict[str, Any],
        cause: str
    ) -> Tuple[int, str]:
        """Compute severity score (0-100) and recommendation string.

        Factors evaluated:
        1. AQI baseline impact (0 to 45 pts)
        2. Population density weight (0 to 15 pts)
        3. Sensitive receptors - Schools & Hospitals (0 to 20 pts)
        4. Weather & Forecast indicators (0 to 10 pts)
        5. Historical trend & spike magnitude (0 to 10 pts)

        Args:
            aqi: Current AQI value.
            population_density_str: String representation of population density.
            nearby_objects: Detected nearby infrastructure.
            weather: Weather information dictionary.
            timeline_info: Historical timeline analysis dictionary.
            cause: Inferred cause string.

        Returns:
            Tuple of (severity_score: int [0-100], recommendation: str).
        """
        logger.info(f"Computing severity score for AQI={aqi}, cause='{cause}'")

        # 1. AQI Score (max 45 points)
        # Scale AQI from 0..500 to 0..45 points
        aqi_pts = min(45.0, (aqi / 500.0) * 45.0)

        # 2. Population Density Score (max 15 points)
        pop_pts = 8.0  # default medium
        density_lower = population_density_str.lower()
        if "high" in density_lower or "dense" in density_lower or "15,000" in density_lower or "12,000" in density_lower:
            pop_pts = 15.0
        elif "medium" in density_lower or "mixed" in density_lower or "8,500" in density_lower:
            pop_pts = 10.0
        elif "low" in density_lower or "suburban" in density_lower or "5,200" in density_lower:
            pop_pts = 5.0

        # 3. Sensitive Receptors - Schools & Hospitals (max 20 points)
        receptor_pts = 0.0
        categories = [obj.get("category", "").lower() for obj in nearby_objects]
        
        school_count = sum(1 for c in categories if "school" in c)
        hospital_count = sum(1 for c in categories if "hospital" in c)

        if school_count > 0:
            receptor_pts += min(10.0, school_count * 8.0)
        if hospital_count > 0:
            receptor_pts += min(10.0, hospital_count * 10.0)
        receptor_pts = min(20.0, receptor_pts)

        # 4. Forecast & Weather (max 10 points)
        # Low wind speed (< 5 km/h) retains pollution -> higher severity
        weather_pts = 4.0
        wind_speed = weather.get("wind_speed", 5.0)
        if wind_speed < 4.0:
            weather_pts += 5.0
        elif wind_speed < 8.0:
            weather_pts += 3.0

        if weather.get("condition", "").lower() in ["fog", "stagnant", "smog", "haze"]:
            weather_pts += 1.0
        weather_pts = min(10.0, weather_pts)

        # 5. Historical Trend & Spike (max 10 points)
        trend_pts = 0.0
        if timeline_info.get("is_spike", False):
            trend_pts += 5.0
        if timeline_info.get("trend_direction") == "RISING":
            trend_pts += 5.0
        trend_pts = min(10.0, trend_pts)

        total_score = int(round(aqi_pts + pop_pts + receptor_pts + weather_pts + trend_pts))
        severity_score = max(0, min(100, total_score))

        # Generate recommendation based on severity score tier and cause
        recommendation = self._generate_recommendation(severity_score, cause, hospital_count > 0, school_count > 0)

        logger.info(f"Calculated severity score: {severity_score}, Recommendation: '{recommendation}'")
        return severity_score, recommendation

    def _generate_recommendation(
        self,
        severity: int,
        cause: str,
        has_hospital: bool,
        has_school: bool
    ) -> str:
        """Derive targeted recommendation string based on severity score and context."""
        if severity >= 85:
            if cause == "Construction Dust":
                return "Immediate inspection and temporary work stoppage at active construction site."
            elif cause == "Industrial Emissions":
                return "Immediate inspection of industrial emission stacks and automated threshold alerting."
            elif cause == "Traffic Congestion":
                return "Deploy traffic diversion protocol and issue immediate public health advisory."
            elif cause == "Crop Burning":
                return "Dispatch enforcement squad for emergency agricultural fire suppression."
            else:
                return "Immediate inspection and emergency response deployment."
        elif severity >= 70:
            if has_hospital or has_school:
                return "Issue vulnerable group health advisory for nearby schools and hospitals."
            return "Increase monitoring frequency and dispatch field inspection team."
        elif severity >= 50:
            return "Notify local municipal authority and monitor trend progression."
        else:
            return "Routine ambient air monitoring."
