# tests/test_retry.py
import pytest
from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted, InvalidArgument
from nanobananapro_mcp.retry import RetryConfig, is_retryable_error


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


class TestIsRetryableError:
    def test_service_unavailable_is_retryable(self):
        error = ServiceUnavailable("Model overloaded")
        assert is_retryable_error(error) is True

    def test_resource_exhausted_is_retryable(self):
        error = ResourceExhausted("Rate limit exceeded")
        assert is_retryable_error(error) is True

    def test_invalid_argument_not_retryable(self):
        error = InvalidArgument("Bad request")
        assert is_retryable_error(error) is False

    def test_generic_exception_not_retryable(self):
        error = ValueError("Something else")
        assert is_retryable_error(error) is False
