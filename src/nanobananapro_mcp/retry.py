"""Retry configuration and utilities for Gemini API calls."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RetryConfig:
    """Configuration for API retry behavior."""

    enabled: bool = True
    initial_delay: float = 2.0
    max_delay: float = 60.0
    multiplier: float = 2.0
    timeout: float = 180.0


from google.api_core import retry, retry_async
from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted

RETRYABLE_EXCEPTIONS = (ServiceUnavailable, ResourceExhausted)


def is_retryable_error(error: Exception) -> bool:
    """Check if an error should trigger a retry."""
    return isinstance(error, RETRYABLE_EXCEPTIONS)


def on_retry_error(error: Exception) -> None:
    """Callback invoked on each retry attempt."""
    logger.warning(f"Retrying after {type(error).__name__}: {error}")


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
        on_error=on_retry_error,
    )


DEFAULT_RETRY = create_retry_decorator(RetryConfig())


def create_async_retry_decorator(config: RetryConfig):
    """Create an async retry decorator from configuration."""
    if not config.enabled:
        return lambda f: f

    return retry_async.AsyncRetry(
        predicate=retry_async.if_exception_type(*RETRYABLE_EXCEPTIONS),
        initial=config.initial_delay,
        maximum=config.max_delay,
        multiplier=config.multiplier,
        timeout=config.timeout,
        on_error=on_retry_error,
    )


DEFAULT_ASYNC_RETRY = create_async_retry_decorator(RetryConfig())
