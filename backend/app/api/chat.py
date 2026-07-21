"""
API route: POST /chat

Accepts a chat query and returns a response from Groq LLM model.
"""

import logging
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status

from app.services.llm.groq_client import GroqClient, GroqClientError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["AI Chatbot"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


SYSTEM_PROMPT = (
    "You are AERIS AI, a high-precision AI assistant for the AERIS Urban Air Quality Intelligence Platform. "
    "Your role is to assist city officials, environmental planners, health authorities, and citizens "
    "with real-time air quality insights, pollutant impact analysis (PM2.5, PM10, SO2, NO2, AQI levels), "
    "mitigation policies, public health advisories, and environmental compliance. "
    "Provide clear, professional, structured, and actionable answers with helpful markdown formatting."
)


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_agent(req: ChatRequest) -> ChatResponse:
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        client = GroqClient()
        response_text = await client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=req.message,
        )
        return ChatResponse(response=response_text)
    except GroqClientError as exc:
        logger.error("Groq Chat client error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to receive a response from Groq AI service.",
        ) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error in chat endpoint")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while generating response.",
        ) from exc
