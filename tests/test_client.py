import pytest
from unittest.mock import Mock, patch, MagicMock

from google.api_core.exceptions import ServiceUnavailable
from nanobananapro_mcp.client import GeminiImageClient, ImageGenerationResult


class TestGeminiImageClient:
    def test_initialization_requires_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="GEMINI_API_KEY"):
                GeminiImageClient()

    def test_initialization_with_env_key(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_client:
                client = GeminiImageClient()
                assert client._client is not None


class TestImageGenerationResult:
    def test_from_response_extracts_text(self):
        mock_part = Mock()
        mock_part.text = "Generated description"
        mock_part.inline_data = None
        mock_response = Mock()
        mock_response.parts = [mock_part]

        result = ImageGenerationResult.from_response(mock_response)
        assert result.text == "Generated description"
        assert result.image_data is None

    def test_from_response_extracts_image(self):
        mock_part = Mock()
        mock_part.text = None
        mock_part.inline_data = Mock()
        mock_part.inline_data.data = b"fake_image_data"
        mock_part.inline_data.mime_type = "image/png"
        mock_response = Mock()
        mock_response.parts = [mock_part]

        result = ImageGenerationResult.from_response(mock_response)
        assert result.text is None
        assert result.image_data == b"fake_image_data"
        assert result.mime_type == "image/png"


class TestGenerateImageRetry:
    def test_retries_on_service_unavailable(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_genai:
                mock_client_instance = Mock()
                mock_genai.return_value = mock_client_instance

                # First call fails, second succeeds
                mock_part = Mock()
                mock_part.text = "Success"
                mock_part.inline_data = None
                mock_response = Mock()
                mock_response.parts = [mock_part]

                mock_client_instance.models.generate_content.side_effect = [
                    ServiceUnavailable("Model overloaded"),
                    mock_response,
                ]

                client = GeminiImageClient()
                result = client.generate_image("test prompt")

                assert result.text == "Success"
                assert mock_client_instance.models.generate_content.call_count == 2
