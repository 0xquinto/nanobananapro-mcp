import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock

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


class TestEditImageRetry:
    def test_retries_on_service_unavailable(self, tmp_path):
        # Create test image
        test_image = tmp_path / "test.png"
        from PIL import Image
        img = Image.new("RGB", (100, 100), color="red")
        img.save(test_image)

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_genai:
                mock_client_instance = Mock()
                mock_genai.return_value = mock_client_instance

                mock_part = Mock()
                mock_part.text = "Edited"
                mock_part.inline_data = None
                mock_response = Mock()
                mock_response.parts = [mock_part]

                mock_client_instance.models.generate_content.side_effect = [
                    ServiceUnavailable("Model overloaded"),
                    mock_response,
                ]

                client = GeminiImageClient()
                result = client.edit_image("edit prompt", test_image)

                assert result.text == "Edited"
                assert mock_client_instance.models.generate_content.call_count == 2


class TestComposeImagesRetry:
    def test_retries_on_service_unavailable(self, tmp_path):
        # Create test images
        test_images = []
        for i in range(2):
            img_path = tmp_path / f"test{i}.png"
            from PIL import Image
            img = Image.new("RGB", (100, 100), color="blue")
            img.save(img_path)
            test_images.append(img_path)

        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_genai:
                mock_client_instance = Mock()
                mock_genai.return_value = mock_client_instance

                mock_part = Mock()
                mock_part.text = "Composed"
                mock_part.inline_data = None
                mock_response = Mock()
                mock_response.parts = [mock_part]

                mock_client_instance.models.generate_content.side_effect = [
                    ServiceUnavailable("Model overloaded"),
                    mock_response,
                ]

                client = GeminiImageClient()
                result = client.compose_images("compose prompt", test_images)

                assert result.text == "Composed"
                assert mock_client_instance.models.generate_content.call_count == 2


class TestSearchGroundedImageRetry:
    def test_retries_on_service_unavailable(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_genai:
                mock_client_instance = Mock()
                mock_genai.return_value = mock_client_instance

                mock_part = Mock()
                mock_part.text = "Grounded"
                mock_part.inline_data = None
                mock_response = Mock()
                mock_response.parts = [mock_part]

                mock_client_instance.models.generate_content.side_effect = [
                    ServiceUnavailable("Model overloaded"),
                    mock_response,
                ]

                client = GeminiImageClient()
                result = client.search_grounded_image("search prompt")

                assert result.text == "Grounded"
                assert mock_client_instance.models.generate_content.call_count == 2


class TestAsyncGenerateImage:
    @pytest.mark.asyncio
    async def test_generate_image_is_async(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}):
            with patch("nanobananapro_mcp.client.genai.Client") as mock_genai:
                mock_client_instance = Mock()
                mock_genai.return_value = mock_client_instance

                mock_part = Mock()
                mock_part.text = "Generated"
                mock_part.inline_data = None
                mock_response = Mock()
                mock_response.parts = [mock_part]

                # Mock the async aio interface
                mock_aio = Mock()
                mock_aio.models.generate_content = AsyncMock(return_value=mock_response)
                mock_client_instance.aio = mock_aio

                client = GeminiImageClient()
                result = await client.generate_image("test prompt")

                assert result.text == "Generated"
                mock_aio.models.generate_content.assert_called_once()
