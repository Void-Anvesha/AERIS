"""
Agent 2: LLM Advisory Agent.

Takes the structured output of the Decision Intelligence Agent and uses
an LLM (via Groq) to generate two natural-language advisories:
1. An operational recommendation for the responsible authority.
2. A plain-language safety advisory for citizens.

All prompt construction is delegated to `prompt_templates.py` - this
module owns orchestration of the LLM calls, concurrency, and error
handling, not prompt text.
"""

import asyncio
import logging
from typing import Optional

from app.schemas.advisory_schema import AdvisoryResponse
from app.schemas.decision_schema import DecisionOutput
from app.services.agents import prompt_templates
from app.services.llm.groq_client import GroqClient, GroqClientError

logger = logging.getLogger(__name__)


class LLMAdvisoryAgentError(RuntimeError):
    """Raised when the LLM Advisory Agent fails to produce an advisory."""


class LLMAdvisoryAgent:
    """Generates authority and citizen advisories from a `DecisionOutput`.

    The agent is stateless aside from its Groq client dependency, making
    it trivial to unit test with a mocked/stubbed `GroqClient`.
    """

    def __init__(self, groq_client: Optional[GroqClient] = None) -> None:
        self._groq_client = groq_client or GroqClient()

    async def generate_advisory(self, decision: DecisionOutput) -> AdvisoryResponse:
        """Generate both advisories concurrently for lower end-to-end latency.

        Args:
            decision: The structured output of the Decision Intelligence Agent.

        Returns:
            An `AdvisoryResponse` containing both generated advisories.

        Raises:
            LLMAdvisoryAgentError: If either LLM call fails.
        """
        authority_prompt = prompt_templates.build_authority_prompt(decision)
        citizen_prompt = prompt_templates.build_citizen_prompt(decision)

        try:
            authority_advisory, citizen_advisory = await asyncio.gather(
                self._groq_client.generate(
                    system_prompt=prompt_templates.AUTHORITY_SYSTEM_PROMPT,
                    user_prompt=authority_prompt,
                ),
                self._groq_client.generate(
                    system_prompt=prompt_templates.CITIZEN_SYSTEM_PROMPT,
                    user_prompt=citizen_prompt,
                ),
            )
        except GroqClientError as exc:
            logger.error("LLM Advisory Agent failed to generate advisory: %s", exc)
            raise LLMAdvisoryAgentError(str(exc)) from exc

        logger.info(
            "Advisory generated | priority=%s authority=%s",
            decision.priority.value,
            decision.authority,
        )

        return AdvisoryResponse(
            authority_advisory=authority_advisory,
            citizen_advisory=citizen_advisory,
        )
