"""Parent Guardrail execution handler for validating agent inputs and outputs."""

import logging
from typing import Dict, Any, Callable, Type
from pydantic import BaseModel, ValidationError as PydanticValidationError
from app.core.exceptions import ValidationError, AERISException

logger = logging.getLogger(__name__)

class ParentGuardrails:
    """Validator and auditor that runs around all intelligence agents."""

    @staticmethod
    def validate_coordinates(latitude: float, longitude: float) -> None:
        """Verify coordinates are within geographical bounds."""
        if not (-90.0 <= latitude <= 90.0):
            raise ValidationError(f"Latitude must be between -90 and 90. Got: {latitude}")
        if not (-180.0 <= longitude <= 180.0):
            raise ValidationError(f"Longitude must be between -180 and 180. Got: {longitude}")

    @staticmethod
    def run_safe(
        agent_name: str,
        agent_fn: Callable[[], Dict[str, Any]],
        input_schema: Type[BaseModel] | None = None,
        input_data: Dict[str, Any] | None = None,
        confidence_threshold: float = 0.70
    ) -> Dict[str, Any]:
        """Execute an agent function inside validation, safety, and logging guardrails.

        Args:
            agent_name: Name of the agent for audit logging.
            agent_fn: Function executing the agent business logic.
            input_schema: Optional Pydantic model for schema validation.
            input_data: Optional raw input dictionary to validate.
            confidence_threshold: Threshold below which warning flags are set.

        Returns:
            Dictionary containing the agent execution results.
        """
        logger.info(f"Guardrails | Intercepting execution for agent: {agent_name}")

        # 1. Input Schema Validation
        if input_schema and input_data is not None:
            try:
                input_schema(**input_data)
            except PydanticValidationError as ve:
                logger.error(f"Guardrails | Input validation failed for {agent_name}: {str(ve)}")
                raise ValidationError(f"Invalid input schema for {agent_name}: {str(ve)}")

            # 2. Coordinate Validation (if applicable)
            lat = input_data.get("latitude") or input_data.get("lat")
            lon = input_data.get("longitude") or input_data.get("lng") or input_data.get("lon")
            if lat is not None and lon is not None:
                ParentGuardrails.validate_coordinates(float(lat), float(lon))

        # 3. Safe Execution
        try:
            result = agent_fn()
        except ValidationError:
            raise
        except AERISException:
            raise
        except Exception as e:
            logger.exception(f"Guardrails | Execution crashed in {agent_name}: {str(e)}")
            raise AERISException(f"Agent {agent_name} failed: {str(e)}")

        # 4. Output Validation & Hallucination/Confidence Checks
        confidence = result.get("confidence", 1.0)
        if confidence < confidence_threshold:
            logger.warning(f"Guardrails | Agent {agent_name} returned low confidence: {confidence}")
            result["low_confidence_alert"] = True
            result["manual_review_required"] = True

        # Check for empty LLM strings (Hallucination detection baseline)
        for key in ["authority_advisory", "citizen_advisory", "recommendation", "advisory"]:
            if key in result and not result[key]:
                logger.error(f"Guardrails | Detected empty/hallucinated output in {agent_name} for key '{key}'")
                result[key] = "Advisory temporarily unavailable. Please monitor local conditions."
                result["hallucination_detected"] = True

        # 5. Audit Logging
        logger.info(f"Guardrails | Audit log: Agent {agent_name} successfully executed. Confidence: {confidence}")
        return result
