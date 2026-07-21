"""
API route: POST /decision

Accepts a raw air-quality `InsightInput` and returns the structured
`DecisionOutput` computed by the Decision Intelligence Agent (Agent 1).
"""

import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.decision_schema import DecisionOutput
from app.schemas.insight_schema import InsightInput
from app.services.orchestration.decision_workflow import DecisionWorkflow

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/decision", tags=["Decision Intelligence"])


@lru_cache
def get_decision_workflow() -> DecisionWorkflow:
    """FastAPI dependency provider for a shared `DecisionWorkflow` instance."""
    return DecisionWorkflow()


@router.post(
    "",
    response_model=DecisionOutput,
    status_code=status.HTTP_200_OK,
    summary="Compute risk score, priority, authority, and action items for an air-quality insight",
)
async def create_decision(
    insight: InsightInput,
    workflow: DecisionWorkflow = Depends(get_decision_workflow),
) -> DecisionOutput:
    """Evaluate a raw air-quality insight and return the computed decision.

    Args:
        insight: The incoming air-quality insight payload.
        workflow: Injected orchestration workflow.

    Returns:
        The `DecisionOutput` produced by the Decision Intelligence Agent.

    Raises:
        HTTPException: 500 if the rule engine fails unexpectedly.
    """
    try:
        return workflow.run_decision(insight)
    except Exception as exc:  # noqa: BLE001 - convert any internal failure to a clean 500
        logger.exception("Decision Intelligence Agent failed to process insight")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to compute decision for the given insight.",
        ) from exc
