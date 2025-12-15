"""
Structured logging configuration using structlog.
Production-grade logging with JSON output and proper formatting.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.types import EventDict, Processor


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log events."""
    event_dict["service"] = "procedural-game-asset-foundry"
    event_dict["version"] = "0.1.0"
    return event_dict


def setup_logging(log_level: str = "INFO", debug: bool = False) -> None:
    """Configure structured logging for the application."""
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )
    
    # Configure structlog processors
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        add_app_context,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="ISO"),
    ]
    
    if debug:
        # Development: Pretty console output
        processors.extend([
            structlog.dev.ConsoleRenderer(colors=True),
        ])
    else:
        # Production: JSON output
        processors.extend([
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ])
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "") -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)