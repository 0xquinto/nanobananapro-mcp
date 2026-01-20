# tests/test_retry.py
import pytest
from nanobananapro_mcp.retry import RetryConfig


class TestRetryConfig:
    def test_default_values(self):
        config = RetryConfig()
        assert config.enabled is True
        assert config.initial_delay == 2.0
        assert config.max_delay == 60.0
        assert config.multiplier == 2.0
        assert config.timeout == 180.0

    def test_custom_values(self):
        config = RetryConfig(
            enabled=False,
            initial_delay=1.0,
            max_delay=30.0,
            multiplier=1.5,
            timeout=60.0,
        )
        assert config.enabled is False
        assert config.initial_delay == 1.0
