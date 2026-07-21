"""Event Detector module for rule-based pollution cause inference and confidence scoring."""

from typing import Dict, Any, List, Tuple
from app.core.logging import logger


class EventDetector:
    """Detector for inferring environmental pollution causes and calculating confidence scores."""

    VALID_CAUSES = [
        "Construction Dust",
        "Traffic Congestion",
        "Industrial Emissions",
        "Crop Burning",
        "Fireworks",
        "Diesel Generator",
        "Unknown"
    ]

    def __init__(self) -> None:
        """Initialize EventDetector."""
        logger.info("Initializing EventDetector service.")

    def detect_cause(
        self,
        aqi: float,
        pm25: float,
        pm10: float,
        weather: Dict[str, Any],
        nearby_objects: List[Dict[str, Any]],
        timeline_info: Dict[str, Any]
    ) -> Tuple[str, float]:
        """Infer environmental cause of air quality degradation using deterministic rule sets.

        Args:
            aqi: Current AQI value.
            pm25: PM2.5 concentration in ug/m3.
            pm10: PM10 concentration in ug/m3.
            weather: Weather details (temperature, humidity, wind_speed, condition).
            nearby_objects: Detected nearby infrastructure items.
            timeline_info: Timeline analysis dictionary (is_spike, trend_direction, etc.).

        Returns:
            Tuple of (cause_name: str, confidence_score: float).
        """
        logger.info(f"Executing rule-based cause inference: AQI={aqi}, PM2.5={pm25}, PM10={pm10}")

        nearby_categories = [obj.get("category", "").lower() for obj in nearby_objects]
        wind_speed = weather.get("wind_speed", 5.0)
        humidity = weather.get("humidity", 50.0)
        temperature = weather.get("temperature", 25.0)
        is_spike = timeline_info.get("is_spike", False)
        spike_ratio = timeline_info.get("spike_ratio", 1.0)

        # Calculate PM ratio (PM10 vs PM2.5)
        pm_ratio = pm10 / pm25 if pm25 > 0 else 1.0

        # Rule 1: Construction Dust
        # Characterized by high coarse particulate matter (PM10 >> PM2.5), low wind speed, and presence of construction sites
        if ("construction sites" in nearby_categories or "construction site" in nearby_categories) and pm_ratio >= 1.6:
            confidence = 0.91 if wind_speed < 10.0 else 0.82
            logger.info(f"Inferred cause: Construction Dust (confidence: {confidence})")
            return "Construction Dust", confidence

        if pm_ratio >= 2.0 and "construction sites" in nearby_categories:
            confidence = 0.88
            logger.info(f"Inferred cause: Construction Dust (confidence: {confidence})")
            return "Construction Dust", confidence

        # Rule 2: Industrial Emissions
        # Characterized by presence of industrial facilities, sustained high AQI/PM2.5/PM10
        if "industries" in nearby_categories or "industrial" in nearby_categories:
            confidence = 0.89 if aqi >= 180.0 else 0.81
            logger.info(f"Inferred cause: Industrial Emissions (confidence: {confidence})")
            return "Industrial Emissions", confidence

        # Rule 3: Traffic Congestion
        # Characterized by nearby roads, high PM2.5 fine particulates, moderate AQI spike
        if "roads" in nearby_categories or "road" in nearby_categories:
            if pm25 >= 60.0 and pm_ratio < 1.6:
                confidence = 0.86
                logger.info(f"Inferred cause: Traffic Congestion (confidence: {confidence})")
                return "Traffic Congestion", confidence

        # Rule 4: Crop Burning
        # Characterized by severe PM2.5 dominance, high spike ratio, low humidity / dry weather
        if is_spike and spike_ratio >= 1.4 and pm25 >= 120.0 and humidity < 45.0:
            confidence = 0.87
            logger.info(f"Inferred cause: Crop Burning (confidence: {confidence})")
            return "Crop Burning", confidence

        # Rule 5: Fireworks
        # Characterized by extreme sudden spike ratio (>= 1.8), very high AQI spike
        if is_spike and spike_ratio >= 1.8 and aqi >= 250.0:
            confidence = 0.85
            logger.info(f"Inferred cause: Fireworks (confidence: {confidence})")
            return "Fireworks", confidence

        # Rule 6: Diesel Generator
        # Localized fine particulate spike near commercial or mixed infrastructure
        if pm25 >= 90.0 and is_spike and ("schools" in nearby_categories or "hospitals" in nearby_categories):
            confidence = 0.80
            logger.info(f"Inferred cause: Diesel Generator (confidence: {confidence})")
            return "Diesel Generator", confidence

        # Fallback Rule 7: Secondary check on PM ratios or nearby categories
        if pm_ratio >= 1.7:
            logger.info("Inferred cause: Construction Dust via PM ratio fallback.")
            return "Construction Dust", 0.75
        elif pm25 >= 75.0:
            logger.info("Inferred cause: Traffic Congestion via fine particulate fallback.")
            return "Traffic Congestion", 0.72

        logger.info("Inferred cause: Unknown (default fallback).")
        return "Unknown", 0.50
