import asyncio
import pytest
from unittest.mock import Mock, patch


class TestCancellation:
    @pytest.mark.asyncio
    async def test_generate_image_can_be_cancelled(self):
        """Verify that generate_image properly handles cancellation."""
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_genai:
                mock_client_instance = Mock()
                mock_genai.return_value = mock_client_instance

                # Create a slow async mock that can be cancelled
                async def slow_generate(*args, **kwargs):
                    await asyncio.sleep(10)  # Long operation
                    return Mock()

                mock_aio = Mock()
                mock_aio.models.generate_content = slow_generate
                mock_client_instance.aio = mock_aio

                from nanobananapro_mcp.client import GeminiImageClient
                client = GeminiImageClient()

                # Start the task
                task = asyncio.create_task(client.generate_image("test prompt"))

                # Give it a moment to start
                await asyncio.sleep(0.01)

                # Cancel it
                task.cancel()

                # Verify it raises CancelledError
                with pytest.raises(asyncio.CancelledError):
                    await task
