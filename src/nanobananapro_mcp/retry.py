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
