# tests/test_retry.py
import pytest
from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted, InvalidArgument
from unittest.mock import Mock, patch
import logging
from nanobananapro_mcp.retry import RetryConfig, is_retryable_error, create_retry_decorator, on_retry_error, DEFAULT_RETRY


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


class TestCreateRetryDecorator:
    def test_creates_retry_with_default_config(self):
        config = RetryConfig()
        retry_decorator = create_retry_decorator(config)
        # Decorator should be callable
        assert callable(retry_decorator)

    def test_disabled_config_returns_passthrough(self):
        config = RetryConfig(enabled=False)
        retry_decorator = create_retry_decorator(config)

        @retry_decorator
        def my_func():
            return "result"

        assert my_func() == "result"

    def test_retry_uses_config_values(self):
        config = RetryConfig(
            initial_delay=1.0,
            max_delay=10.0,
            multiplier=1.5,
            timeout=30.0,
        )
        with patch("nanobananapro_mcp.retry.retry.Retry") as mock_retry:
            mock_retry.return_value = lambda f: f
            create_retry_decorator(config)
            mock_retry.assert_called_once()
            call_kwargs = mock_retry.call_args.kwargs
            assert call_kwargs["initial"] == 1.0
            assert call_kwargs["maximum"] == 10.0
            assert call_kwargs["multiplier"] == 1.5
            assert call_kwargs["timeout"] == 30.0


class TestOnRetryError:
    def test_logs_warning_on_error(self, caplog):
        error = ServiceUnavailable("Model overloaded")
        with caplog.at_level(logging.WARNING):
            on_retry_error(error)
        assert "Retrying after ServiceUnavailable" in caplog.text
        assert "Model overloaded" in caplog.text


class TestRetryDecoratorWithCallback:
    def test_callback_is_passed_to_retry(self):
        config = RetryConfig()
        with patch("nanobananapro_mcp.retry.retry.Retry") as mock_retry:
            mock_retry.return_value = lambda f: f
            create_retry_decorator(config)
            call_kwargs = mock_retry.call_args.kwargs
            assert "on_error" in call_kwargs


class TestDefaultRetry:
    def test_default_retry_is_callable(self):
        assert callable(DEFAULT_RETRY)


class TestAsyncRetryDecorator:
    def test_creates_async_retry_with_default_config(self):
        from nanobananapro_mcp.retry import create_async_retry_decorator, RetryConfig
        config = RetryConfig()
        retry_decorator = create_async_retry_decorator(config)
        assert callable(retry_decorator)

    def test_async_disabled_config_returns_passthrough(self):
        from nanobananapro_mcp.retry import create_async_retry_decorator, RetryConfig
        import asyncio

        config = RetryConfig(enabled=False)
        retry_decorator = create_async_retry_decorator(config)

        @retry_decorator
        async def my_func():
            return "result"

        assert asyncio.run(my_func()) == "result"


class TestDefaultAsyncRetry:
    def test_default_async_retry_is_callable(self):
        from nanobananapro_mcp.retry import DEFAULT_ASYNC_RETRY
        assert callable(DEFAULT_ASYNC_RETRY)
