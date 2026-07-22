"""
Thin, reusable async wrapper around the Groq API.

Groq exposes an OpenAI-compatible `/chat/completions` endpoint, so we
reuse the official `openai` async SDK pointed at Groq's base URL instead
of hand-rolling HTTP calls. Keeping this in a single module means every
agent that needs an LLM call shares one client, one timeout policy, and
one error-handling strategy.
"""

import logging
from typing import Optional

from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncOpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class GroqClientError(RuntimeError):
    """Raised when the Groq API cannot be reached or returns an error."""


class GroqClient:
    """Reusable async client for chat-completion calls against Groq.

    Designed to be instantiated once (e.g. as a FastAPI dependency /
    singleton) and reused across requests, since the underlying HTTP
    client pools connections internally.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> None:
        settings = get_settings()
        self._model = model or settings.GROQ_MODEL
        self._temperature = settings.GROQ_TEMPERATURE
        self._max_tokens = settings.GROQ_MAX_TOKENS

        api_key_val = api_key or settings.GROQ_API_KEY
        if not api_key_val:
            api_key_val = "none" # Fallback dummy value to avoid startup validation error

        self._client = AsyncOpenAI(
            api_key=api_key_val,
            base_url=base_url or settings.GROQ_BASE_URL,
            timeout=timeout or settings.GROQ_REQUEST_TIMEOUT_SECONDS,
        )

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Send a single chat-completion request and return the text reply.

        Args:
            system_prompt: Instructions establishing the assistant's role/behaviour.
            user_prompt: The task-specific prompt (built from `prompt_templates.py`).

        Returns:
            The stripped text content of the model's first response choice.

        Raises:
            GroqClientError: If the request times out, cannot connect, or
                Groq returns a non-2xx status code.
        """
        try:
            completion = await self._client.chat.completions.create(
                model=self._model,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
        except APITimeoutError as exc:
            logger.error("Groq API request timed out: %s", exc)
            raise GroqClientError("The Groq API request timed out.") from exc
        except APIConnectionError as exc:
            logger.error("Failed to connect to Groq API: %s", exc)
            raise GroqClientError("Could not connect to the Groq API.") from exc
        except APIStatusError as exc:
            logger.error("Groq API returned an error status %s: %s", exc.status_code, exc.message)
            raise GroqClientError(f"Groq API error ({exc.status_code}): {exc.message}") from exc

        content = completion.choices[0].message.content if completion.choices else None
        if not content:
            logger.warning("Groq API returned an empty completion.")
            raise GroqClientError("Groq API returned an empty response.")

        return content.strip()
