"""Timeline analysis module for historical AQI tracking and spike detection."""

from typing import List, Dict, Any
from app.core.logging import logger


class TimelineAnalyzer:
    """Analyzer for processing historical air quality readings and detecting temporal spikes."""

    def __init__(self, spike_threshold_ratio: float = 1.25) -> None:
        """Initialize TimelineAnalyzer.

        Args:
            spike_threshold_ratio: Multiplier threshold above baseline average to flag an AQI spike.
        """
        self.spike_threshold_ratio = spike_threshold_ratio
        logger.info(f"Initialized TimelineAnalyzer with spike threshold ratio {spike_threshold_ratio}.")

    def analyze_history(
        self,
        current_aqi: float,
        current_pm25: float,
        current_pm10: float,
        history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze historical AQI trend and detect presence of AQI/PM spikes.

        Args:
            current_aqi: Current AQI reading.
            current_pm25: Current PM2.5 reading.
            current_pm10: Current PM10 reading.
            history: List of historical reading dicts containing 'aqi', 'pm25', 'pm10', etc.

        Returns:
            Dict containing spike detection metadata, trend direction, baseline average, and spike ratio.
        """
        logger.info(f"Analyzing timeline history across {len(history)} historical entries.")

        if not history:
            logger.warning("No historical readings provided. Assuming default baseline.")
            return {
                "is_spike": current_aqi >= 150.0,
                "baseline_aqi": current_aqi,
                "spike_ratio": 1.0,
                "trend_direction": "STABLE",
                "historical_count": 0
            }

        past_aqis = [item.get("aqi", current_aqi) for item in history if isinstance(item.get("aqi"), (int, float))]
        if not past_aqis:
            past_aqis = [current_aqi]

        baseline_aqi = sum(past_aqis) / len(past_aqis)
        spike_ratio = current_aqi / baseline_aqi if baseline_aqi > 0 else 1.0
        is_spike = spike_ratio >= self.spike_threshold_ratio or (current_aqi >= 200.0 and current_aqi - baseline_aqi >= 30.0)

        # Trend direction
        if len(past_aqis) >= 2:
            recent_avg = past_aqis[-1]
            if current_aqi > recent_avg * 1.1:
                trend_direction = "RISING"
            elif current_aqi < recent_avg * 0.9:
                trend_direction = "FALLING"
            else:
                trend_direction = "STABLE"
        else:
            trend_direction = "RISING" if current_aqi > baseline_aqi else "STABLE"

        result = {
            "is_spike": is_spike,
            "baseline_aqi": round(baseline_aqi, 2),
            "spike_ratio": round(spike_ratio, 2),
            "trend_direction": trend_direction,
            "historical_count": len(history)
        }

        logger.debug(f"Timeline analysis result: {result}")
        return result
