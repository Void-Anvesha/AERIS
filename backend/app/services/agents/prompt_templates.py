"""
Prompt templates for the LLM Advisory Agent.

All prompt text lives here (never inline in agent/service code) so that
prompts can be reviewed, versioned, and tuned independently of the
business logic that calls them.
"""

from app.schemas.decision_schema import DecisionOutput

# --------------------------------------------------------------------------
# System prompts - establish role, tone, and output constraints.
# --------------------------------------------------------------------------

AUTHORITY_SYSTEM_PROMPT = (
    "You are AERIS, an AI advisory system that supports municipal and pollution "
    "control authorities in responding to urban air-quality emergencies. "
    "You write concise, operational, field-ready instructions for government "
    "officials and enforcement teams. Always respond with a numbered list of "
    "clear, concrete action items. Do not include disclaimers, greetings, or "
    "explanations - only the action list."
)

CITIZEN_SYSTEM_PROMPT = (
    "You are AERIS, a public health advisory assistant that communicates air "
    "quality risks to the general public in plain, reassuring, and easy to "
    "follow language. Your audience includes children, elderly people, and "
    "people without a technical background. Always respond with a short "
    "numbered list of practical precautions. Do not include disclaimers, "
    "greetings, or explanations - only the advisory list."
)


def _build_context_block(decision: DecisionOutput) -> str:
    """Render the shared factual context block used by both prompt types.

    Keeping this in one place guarantees the authority and citizen prompts
    are always grounded in the exact same underlying decision data.
    """
    return (
        f"Priority: {decision.priority.value}\n"
        f"Risk Score: {decision.risk_score}/100\n"
        f"Current AQI: {decision.aqi}\n"
        f"Forecasted AQI: {decision.forecast}\n"
        f"Dominant Pollutant: {decision.dominant_pollutant}\n"
        f"Attributed Source: {decision.source}\n"
        f"Responsible Authority: {decision.authority}\n"
        f"Required Response Time: {decision.response_time}\n"
        f"Zone: {decision.zone_name or 'Unspecified'}\n"
        f"Key Reasons:\n- " + "\n- ".join(decision.reason or ["Not specified"]) + "\n"
        f"Preliminary Recommended Actions:\n- "
        + "\n- ".join(decision.recommended_actions or ["Not specified"])
    )


def build_authority_prompt(decision: DecisionOutput) -> str:
    """Build the user prompt requesting authority-facing recommendations.

    Args:
        decision: The structured output of the Decision Intelligence Agent.

    Returns:
        A fully-formed user prompt string ready to send to the LLM.
    """
    context = _build_context_block(decision)
    return (
        "Given the following air-quality decision context, generate a numbered "
        "list of specific, operational actions the responsible authority should "
        "take immediately, in priority order. Focus on inspection, enforcement, "
        "mitigation, and monitoring measures relevant to the attributed source "
        "and dominant pollutant.\n\n"
        f"{context}\n\n"
        "Respond with only the numbered action list."
    )


def build_citizen_prompt(decision: DecisionOutput) -> str:
    """Build the user prompt requesting a citizen-facing advisory.

    Args:
        decision: The structured output of the Decision Intelligence Agent.

    Returns:
        A fully-formed user prompt string ready to send to the LLM.
    """
    context = _build_context_block(decision)
    return (
        "Given the following air-quality decision context, generate a numbered "
        "list of clear, practical precautions for the general public, "
        "including specific guidance for sensitive groups such as children, "
        "the elderly, and people with respiratory conditions where relevant.\n\n"
        f"{context}\n\n"
        "Respond with only the numbered advisory list."
    )
