"""Retry configuration and utilities for Gemini API calls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RetryConfig:
    """Configuration for API retry behavior."""

    enabled: bool = True
    initial_delay: float = 2.0
    max_delay: float = 60.0
    multiplier: float = 2.0
    timeout: float = 180.0


from google.api_core import retry
from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted

RETRYABLE_EXCEPTIONS = (ServiceUnavailable, ResourceExhausted)


def is_retryable_error(error: Exception) -> bool:
    """Check if an error should trigger a retry."""
    return isinstance(error, RETRYABLE_EXCEPTIONS)


def create_retry_decorator(config: RetryConfig):
    """Create a retry decorator from configuration."""
    if not config.enabled:
        # Return passthrough decorator
        return lambda f: f

    return retry.Retry(
        predicate=retry.if_exception_type(*RETRYABLE_EXCEPTIONS),
        initial=config.initial_delay,
        maximum=config.max_delay,
        multiplier=config.multiplier,
        timeout=config.timeout,
    )
