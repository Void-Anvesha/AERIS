"""
Centralised logging configuration for AERIS.

Import `configure_logging()` once at application startup (see `main.py`)
and use `logging.getLogger(__name__)` everywhere else in the codebase.
"""

import logging
import sys

from app.core.config import get_settings


def configure_logging() -> None:
    """Configure the root logger with a consistent, structured format.

    Idempotent: safe to call multiple times (e.g. in tests) without
    duplicating log handlers.
    """
    settings = get_settings()
    root_logger = logging.getLogger()

    if root_logger.handlers:
        # Already configured (e.g. re-imported in tests) - avoid duplicate handlers.
        root_logger.setLevel(settings.LOG_LEVEL)
        return

    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)
    root_logger.setLevel(settings.LOG_LEVEL)
