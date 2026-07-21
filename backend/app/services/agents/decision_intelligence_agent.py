"""
Agent 1: Decision Intelligence Agent.

A deterministic, explainable rule engine that turns a raw air-quality
`InsightInput` into a structured `DecisionOutput`: risk score, priority,
responsible authority, response SLA, recommended actions, and the
reasoning behind each decision. No LLM calls happen here by design -
this agent must be fast, auditable, and reproducible.
"""

import logging

from app.core.config import get_settings
from app.schemas.decision_schema import DecisionOutput, Priority
from app.schemas.insight_schema import InsightInput, PopulationDensity

logger = logging.getLogger(__name__)


class DecisionIntelligenceAgent:
    """Rule-based decision engine for urban air-quality incidents.

    The scoring model is intentionally simple and fully documented so it
    can be audited, unit-tested, and tuned by domain experts without
    touching the surrounding orchestration/API code.
    """

    # --- Scoring weights (tunable constants) -------------------------------
    _AQI_SCORE_CAP = 70  # Max points contributed by AQI magnitude alone.
    _AQI_SCALE_REFERENCE = 400  # AQI value considered "maximum severity" for scaling.
    _FORECAST_INCREASE_WEIGHT = 10
    _HOTSPOT_WEIGHT = 10
    _SCHOOLS_WEIGHT = 8
    _HOSPITALS_WEIGHT = 8
    _HIGH_DENSITY_WEIGHT = 8
    _MEDIUM_DENSITY_WEIGHT = 4

    # --- Priority thresholds (based directly on current AQI) --------------
    _CRITICAL_AQI_THRESHOLD = 300
    _HIGH_AQI_THRESHOLD = 200
    _MEDIUM_AQI_THRESHOLD = 100

    _SCHOOLS_RISK_THRESHOLD = 2
    _HOSPITALS_RISK_THRESHOLD = 1

    _RESPONSE_TIME_BY_PRIORITY = {
        Priority.CRITICAL: "Within 2 Hours",
        Priority.HIGH: "Within 6 Hours",
        Priority.MEDIUM: "Within 24 Hours",
        Priority.LOW: "Within 72 Hours",
    }

    _AUTHORITY_BY_SOURCE = {
        "construction": "Municipal Corporation",
        "vehicular": "Traffic Police & Transport Department",
        "traffic": "Traffic Police & Transport Department",
        "industrial": "State Pollution Control Board",
        "industry": "State Pollution Control Board",
        "stubble burning": "Agriculture Department & State Pollution Control Board",
        "crop burning": "Agriculture Department & State Pollution Control Board",
        "waste burning": "Municipal Corporation & State Pollution Control Board",
        "dust": "Municipal Corporation",
    }
    _DEFAULT_AUTHORITY = "State Pollution Control Board"

    def __init__(self) -> None:
        self._settings = get_settings()

    def evaluate(self, insight: InsightInput) -> DecisionOutput:
        """Run the full rule engine over a single air-quality insight.

        Args:
            insight: Validated raw insight payload.

        Returns:
            A fully populated `DecisionOutput`.
        """
        reasons: list[str] = []

        priority = self._determine_priority(insight.aqi)
        reasons.append(self._priority_reason(insight.aqi, priority))

        risk_score, score_reasons = self._calculate_risk_score(insight)
        reasons.extend(score_reasons)

        manual_review = insight.confidence < self._settings.MANUAL_REVIEW_CONFIDENCE_THRESHOLD
        if manual_review:
            reasons.append(
                f"Forecast confidence ({insight.confidence:.2f}) is below the "
                f"{self._settings.MANUAL_REVIEW_CONFIDENCE_THRESHOLD:.2f} trust threshold - "
                "flagged for manual review"
            )

        authority = self._determine_authority(insight.source, priority)
        response_time = self._RESPONSE_TIME_BY_PRIORITY[priority]
        actions = self._generate_action_items(insight, priority)

        logger.info(
            "Decision computed | aqi=%s priority=%s risk_score=%s authority=%s manual_review=%s",
            insight.aqi,
            priority.value,
            risk_score,
            authority,
            manual_review,
        )

        return DecisionOutput(
            risk_score=risk_score,
            priority=priority,
            authority=authority,
            response_time=response_time,
            recommended_actions=actions,
            reason=reasons,
            manual_review_required=manual_review,
            aqi=insight.aqi,
            forecast=insight.forecast,
            dominant_pollutant=insight.dominant_pollutant,
            source=insight.source,
            zone_name=insight.zone_name,
        )

    # ------------------------------------------------------------------
    # Priority
    # ------------------------------------------------------------------
    def _determine_priority(self, aqi: float) -> Priority:
        """Map current AQI to a priority band."""
        if aqi > self._CRITICAL_AQI_THRESHOLD:
            return Priority.CRITICAL
        if aqi > self._HIGH_AQI_THRESHOLD:
            return Priority.HIGH
        if aqi > self._MEDIUM_AQI_THRESHOLD:
            return Priority.MEDIUM
        return Priority.LOW

    def _priority_reason(self, aqi: float, priority: Priority) -> str:
        band = {
            Priority.CRITICAL: "> 300 (Critical band)",
            Priority.HIGH: "in the 201-300 range (High band)",
            Priority.MEDIUM: "in the 101-200 range (Medium band)",
            Priority.LOW: "<= 100 (Low band)",
        }[priority]
        return f"Current AQI ({aqi:g}) is {band}"

    # ------------------------------------------------------------------
    # Risk score
    # ------------------------------------------------------------------
    def _calculate_risk_score(self, insight: InsightInput) -> tuple[int, list[str]]:
        """Compute a composite 0-100 risk score with a human-readable trail.

        The score blends the raw AQI magnitude (capped contribution) with
        additive risk factors for worsening trend, hotspot status, and
        exposure sensitivity (schools, hospitals, population density).
        """
        reasons: list[str] = []

        aqi_component = min(
            self._AQI_SCORE_CAP,
            (insight.aqi / self._AQI_SCALE_REFERENCE) * self._AQI_SCORE_CAP,
        )
        score = aqi_component

        if insight.forecast > insight.aqi:
            score += self._FORECAST_INCREASE_WEIGHT
            reasons.append(
                f"Forecast AQI ({insight.forecast:g}) is higher than current AQI, "
                "indicating a worsening trend"
            )

        if insight.hotspot:
            score += self._HOTSPOT_WEIGHT
            reasons.append("Zone flagged as a persistent pollution hotspot")

        if insight.nearby_schools > self._SCHOOLS_RISK_THRESHOLD:
            score += self._SCHOOLS_WEIGHT
            reasons.append(
                f"{insight.nearby_schools} schools located within the affected radius"
            )

        if insight.nearby_hospitals > self._HOSPITALS_RISK_THRESHOLD:
            score += self._HOSPITALS_WEIGHT
            reasons.append(
                f"{insight.nearby_hospitals} hospitals located within the affected radius"
            )

        if insight.population_density == PopulationDensity.HIGH:
            score += self._HIGH_DENSITY_WEIGHT
            reasons.append("High population density increases exposure risk")
        elif insight.population_density == PopulationDensity.MEDIUM:
            score += self._MEDIUM_DENSITY_WEIGHT
            reasons.append("Medium population density moderately increases exposure risk")

        clamped_score = max(0, min(100, round(score)))
        return clamped_score, reasons

    # ------------------------------------------------------------------
    # Authority
    # ------------------------------------------------------------------
    def _determine_authority(self, source: str, priority: Priority) -> str:
        """Resolve the responsible authority from the attributed source.

        Critical incidents additionally loop in the Disaster Management
        Authority regardless of source, since cross-agency coordination is
        typically required at that severity.
        """
        authority = self._AUTHORITY_BY_SOURCE.get(source.strip().lower(), self._DEFAULT_AUTHORITY)
        if priority == Priority.CRITICAL:
            return f"{authority} + District Disaster Management Authority"
        return authority

    # ------------------------------------------------------------------
    # Action items
    # ------------------------------------------------------------------
    def _generate_action_items(self, insight: InsightInput, priority: Priority) -> list[str]:
        """Generate a deterministic, source-aware baseline action list.

        These are preliminary/rule-based actions. The LLM Advisory Agent
        (Agent 2) later expands on these with richer, natural-language
        recommendations for both authorities and citizens.
        """
        actions: list[str] = []
        source_lower = insight.source.strip().lower()

        if "construct" in source_lower or "dust" in source_lower:
            actions.append("Inspect construction sites for dust-control compliance")
            actions.append("Increase road/site water sprinkling in the affected zone")
        elif "vehic" in source_lower or "traffic" in source_lower:
            actions.append("Restrict heavy vehicle movement during peak hours")
            actions.append("Deploy traffic police to manage congestion hotspots")
        elif "industr" in source_lower:
            actions.append("Inspect nearby industrial units for emission compliance")
            actions.append("Issue show-cause notices to non-compliant facilities")
        elif "burning" in source_lower:
            actions.append("Deploy field teams to identify and stop open burning")
            actions.append("Coordinate with agriculture department on residue management")
        else:
            actions.append(f"Investigate reported source ('{insight.source}') for compliance")

        if insight.hotspot:
            actions.append("Deploy anti-smog guns / mobile misting units in the hotspot zone")

        if insight.nearby_schools > self._SCHOOLS_RISK_THRESHOLD:
            actions.append("Advise nearby schools to suspend outdoor activities")

        if insight.nearby_hospitals > self._HOSPITALS_RISK_THRESHOLD:
            actions.append("Alert nearby hospitals to prepare for respiratory admissions")

        if priority in (Priority.CRITICAL, Priority.HIGH):
            actions.append("Increase AQI monitoring frequency to hourly")
        else:
            actions.append("Continue routine AQI monitoring")

        return actions
