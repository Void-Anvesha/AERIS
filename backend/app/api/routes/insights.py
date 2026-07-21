from fastapi import APIRouter

from app.models.insight import IntelligenceSnapshot, SourceAttribution, Hotspot
from app.services.agents.decision_intelligence import DecisionIntelligenceAgent

router = APIRouter(tags=["insights"])


@router.get("/insights", response_model=IntelligenceSnapshot)
def get_insights() -> IntelligenceSnapshot:
    agent = DecisionIntelligenceAgent()
    return agent.generate_snapshot()
