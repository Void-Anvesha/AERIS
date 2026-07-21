from app.models.insight import Hotspot, IntelligenceSnapshot, SourceAttribution


class DecisionIntelligenceAgent:
    def __init__(self) -> None:
        self.city = "Smart City"

    def generate_snapshot(self) -> IntelligenceSnapshot:
        return IntelligenceSnapshot(
            city=self.city,
            current_aqi=168,
            status="Unhealthy",
            trend="Rising",
            forecast_next_24h=182,
            forecast_next_72h=190,
            hotspots=[
                Hotspot(name="Downtown Junction", lat=12.9716, lng=77.5946, risk_level="High", source="Traffic"),
                Hotspot(name="Industrial Corridor", lat=12.9600, lng=77.6200, risk_level="Very High", source="Industry"),
            ],
            source_attribution=SourceAttribution(
                traffic=0.42,
                industry=0.28,
                biomass=0.18,
                dust=0.12,
            ),
            recommendation="Deploy mobile monitoring units, restrict truck movement during peak hours, and activate roadside dust suppression.",
            advisory="Sensitive groups should avoid prolonged outdoor activity and keep windows closed. General citizens should use masks if outdoors.",
        )
