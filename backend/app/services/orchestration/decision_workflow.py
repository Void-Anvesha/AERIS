"""
Orchestration layer wiring Agent 1 (Decision Intelligence) and Agent 2
(LLM Advisory) into a single pipeline:

    InsightInput -> DecisionIntelligenceAgent -> DecisionOutput
                                                        |
                                                        v
                                          LLMAdvisoryAgent -> AdvisoryResponse

`POST /decision` uses only the first half of this pipeline.
`POST /advisory` uses only the second half (given an already-computed
`DecisionOutput`). A combined `run_full_pipeline` is exposed for callers
(e.g. batch jobs, internal tooling) that want both steps in one call.
"""

import logging

from app.schemas.advisory_schema import AdvisoryResponse
from app.schemas.decision_schema import DecisionOutput
from app.schemas.insight_schema import InsightInput
from app.services.agents.decision_intelligence_agent import DecisionIntelligenceAgent
from app.services.agents.llm_advisory_agent import LLMAdvisoryAgent

logger = logging.getLogger(__name__)


class DecisionWorkflow:
    """Coordinates the Decision Intelligence and LLM Advisory agents.

    This class contains no business rules or prompt logic itself - it is
    purely a thin composition layer, keeping each agent independently
    reusable and testable.
    """

    def __init__(
        self,
        decision_agent: DecisionIntelligenceAgent | None = None,
        advisory_agent: LLMAdvisoryAgent | None = None,
    ) -> None:
        self._decision_agent = decision_agent or DecisionIntelligenceAgent()
        self._advisory_agent = advisory_agent or LLMAdvisoryAgent()

    def run_decision(self, insight: InsightInput) -> DecisionOutput:
        """Run Agent 1 only: raw insight -> decision.

        Args:
            insight: Validated raw air-quality insight.

        Returns:
            The computed `DecisionOutput`.
        """
        logger.debug("Running decision step for zone=%s", insight.zone_name)
        return self._decision_agent.evaluate(insight)

    async def run_advisory(self, decision: DecisionOutput, language: str = "English") -> AdvisoryResponse:
        """Run Agent 2 only: decision -> advisory (authority + citizen).

        Args:
            decision: A previously computed `DecisionOutput`.
            language: Language for citizen advisory.

        Returns:
            The generated `AdvisoryResponse`.
        """
        logger.debug("Running advisory step for priority=%s", decision.priority.value)
        return await self._advisory_agent.generate_advisory(decision, language=language)


    async def run_full_pipeline(self, insight: InsightInput) -> tuple[DecisionOutput, AdvisoryResponse]:
        """Run the complete pipeline: raw insight -> decision -> advisory.

        Args:
            insight: Validated raw air-quality insight.

        Returns:
            A tuple of `(DecisionOutput, AdvisoryResponse)`.
        """
        decision = self.run_decision(insight)
        advisory = await self.run_advisory(decision)
        return decision, advisory
