from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from app.core.logging import logger


@dataclass
class AgentCheckpoint:
    name: str
    status: str
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)


class OrchestratorAgent:
    """Coordinates agent execution with fallback and checkpointing safeguards."""

    def __init__(self) -> None:
        self.checkpoints: List[AgentCheckpoint] = []
        self.last_known_good_state: Optional[Dict[str, Any]] = None

    def run(self, agents: List[tuple[str, Callable[[], Dict[str, Any]]]]) -> Dict[str, Any]:
        self.checkpoints = []
        for name, agent_fn in agents:
            try:
                self._record_checkpoint(name, "running", "Agent started")
                result = agent_fn()
                self.last_known_good_state = result
                self._record_checkpoint(name, "completed", "Agent completed successfully", result)
            except Exception as exc:  # pragma: no cover - guardrail path
                logger.exception("Agent %s failed: %s", name, str(exc))
                self._record_checkpoint(name, "failed", f"Agent failed: {exc}", {"error": str(exc)})
                return self._fallback_state(name, str(exc))

        return {
            "status": "completed",
            "checkpoints": [checkpoint.__dict__ for checkpoint in self.checkpoints],
            "last_known_good_state": self.last_known_good_state or {},
        }

    def _record_checkpoint(self, name: str, status: str, message: str, payload: Optional[Dict[str, Any]] = None) -> None:
        self.checkpoints.append(AgentCheckpoint(name=name, status=status, message=message, payload=payload or {}))

    def _fallback_state(self, failed_agent: str, error: str) -> Dict[str, Any]:
        return {
            "status": "fallback",
            "failed_agent": failed_agent,
            "error": error,
            "checkpoints": [checkpoint.__dict__ for checkpoint in self.checkpoints],
            "last_known_good_state": self.last_known_good_state or {},
        }
