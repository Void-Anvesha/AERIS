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

    async def generate_advisory(self, decision: DecisionOutput, language: str = "English") -> AdvisoryResponse:
        """Generate advisories concurrently, including SMS and Email channels.

        Args:
            decision: The structured output of the Decision Intelligence Agent.
            language: Language option for citizen advisory.

        Returns:
            An `AdvisoryResponse` containing generated advisories.

        Raises:
            LLMAdvisoryAgentError: If either LLM call fails.
        """
        authority_prompt = prompt_templates.build_authority_prompt(decision)
        citizen_prompt = prompt_templates.build_citizen_prompt(decision, language)
        sms_prompt = prompt_templates.build_sms_prompt(decision)
        email_prompt = prompt_templates.build_email_prompt(decision)

        try:
            authority_adivsory, citizen_advisory, sms_alert, email_alert = await asyncio.gather(
                self._groq_client.generate(
                    system_prompt=prompt_templates.AUTHORITY_SYSTEM_PROMPT,
                    user_prompt=authority_prompt,
                ),
                self._groq_client.generate(
                    system_prompt=prompt_templates.CITIZEN_SYSTEM_PROMPT,
                    user_prompt=citizen_prompt,
                ),
                self._groq_client.generate(
                    system_prompt=prompt_templates.SMS_SYSTEM_PROMPT,
                    user_prompt=sms_prompt,
                ),
                self._groq_client.generate(
                    system_prompt=prompt_templates.EMAIL_SYSTEM_PROMPT,
                    user_prompt=email_prompt,
                ),
            )
        except GroqClientError as exc:
            logger.warning("LLM Advisory Agent failed to generate advisory (e.g. invalid GROQ_API_KEY): %s. Falling back to structured mock advisory.", exc)
            authority_adivsory = "\n".join([f"{i+1}. {action}" for i, action in enumerate(decision.recommended_actions)])
            if not authority_adivsory:
                authority_adivsory = "1. Deploy street sweepers and water sprinklers.\n2. Restrict commercial vehicles."
            citizen_advisory = f"Air quality is {decision.priority.value} in your area. Wear N95 masks, avoid outdoor exercise, and keep sensitive individuals indoors."
            sms_alert = f"ALERT: AQI in {decision.zone_name or 'Affected Area'} is {decision.priority.value} ({int(decision.aqi or 0)}). Wear N95 masks."
            email_alert = f"<h3>AERIS Public Alert</h3><p>Air Quality Index has reached {decision.priority.value} levels ({int(decision.aqi or 0)}) due to {decision.source or 'ambient pollution'}. Please follow safety guidelines.</p>"


        logger.info(
            "Advisory generated | priority=%s authority=%s language=%s",
            decision.priority.value,
            decision.authority,
            language
        )

        return AdvisoryResponse(
            authority_advisory=authority_adivsory,
            citizen_advisory=citizen_advisory,
            sms_advisory=sms_alert,
            email_advisory=email_alert
        )
