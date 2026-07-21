"""Hotspot and Event Detection service package for AERIS platform."""

from app.services.hotspot.hotspot_agent import (
    HotspotAgent,
    HotspotInput,
    HotspotOutput,
)
from app.services.hotspot.timeline import TimelineAnalyzer
from app.services.hotspot.cluster_detector import ClusterDetector
from app.services.hotspot.event_detector import EventDetector
from app.services.hotspot.severity import SeverityCalculator

__all__ = [
    "HotspotAgent",
    "HotspotInput",
    "HotspotOutput",
    "TimelineAnalyzer",
    "ClusterDetector",
    "EventDetector",
    "SeverityCalculator",
]
