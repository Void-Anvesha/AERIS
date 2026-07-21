"""
Schema describing the output of the LLM Advisory Agent.
"""

from pydantic import BaseModel, Field


class AdvisoryResponse(BaseModel):
    """Final advisory pair generated from a `DecisionOutput`.

    Attributes:
        authority_advisory: Actionable guidance addressed to the responsible authority.
        citizen_advisory: Plain-language, public-facing safety guidance.
    """

    authority_advisory: str = Field(..., description="Actionable guidance for the responsible authority")
    citizen_advisory: str = Field(..., description="Public-facing citizen safety advisory")

    model_config = {
        "json_schema_extra": {
            "example": {
                "authority_advisory": (
                    "1. Inspect construction sites for dust-control compliance.\n"
                    "2. Increase road sprinkling frequency in the hotspot zone.\n"
                    "3. Restrict heavy vehicle movement during peak hours.\n"
                    "4. Monitor AQI hourly until levels fall below 200."
                ),
                "citizen_advisory": (
                    "Air quality is Critical in your area. Wear N95 masks outdoors, "
                    "avoid outdoor exercise, and keep children and elderly indoors. "
                    "Schools should suspend outdoor sports until conditions improve."
                ),
            }
        }
    }
