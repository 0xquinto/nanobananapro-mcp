"""Tests for seed parameter functionality."""

import pytest
from unittest.mock import AsyncMock, Mock, patch


class TestSeedParameter:
    """Tests for seed parameter in server functions."""

    @pytest.mark.asyncio
    async def test_generate_image_accepts_seed(self):
        """generate_image should accept optional seed parameter."""
        with patch("nanobananapro_mcp.server.get_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client
            mock_result = Mock()
            mock_result.text = "Generated image"
            mock_result.image_data = b"fake_data"
            mock_result.mime_type = "image/png"
            mock_result.grounding_metadata = None
            mock_client.generate_image = AsyncMock(return_value=mock_result)

            from nanobananapro_mcp.server import generate_image

            result = await generate_image(
                prompt="A sunset",
                seed=12345,
            )

            mock_client.generate_image.assert_called_once()
            call_kwargs = mock_client.generate_image.call_args.kwargs
            assert call_kwargs.get("seed") == 12345

    @pytest.mark.asyncio
    async def test_seed_is_optional(self):
        """generate_image should work without seed (defaults to None)."""
        with patch("nanobananapro_mcp.server.get_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client
            mock_result = Mock()
            mock_result.text = "Generated image"
            mock_result.image_data = b"fake_data"
            mock_result.mime_type = "image/png"
            mock_result.grounding_metadata = None
            mock_client.generate_image = AsyncMock(return_value=mock_result)

            from nanobananapro_mcp.server import generate_image

            result = await generate_image(prompt="A sunset")

            mock_client.generate_image.assert_called_once()
            call_kwargs = mock_client.generate_image.call_args.kwargs
            assert call_kwargs.get("seed") is None

    @pytest.mark.asyncio
    async def test_edit_image_accepts_seed(self):
        """edit_image should accept optional seed parameter."""
        with patch("nanobananapro_mcp.server.get_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client
            mock_result = Mock()
            mock_result.text = "Edited image"
            mock_result.image_data = b"fake_data"
            mock_result.mime_type = "image/png"
            mock_result.grounding_metadata = None
            mock_client.edit_image = AsyncMock(return_value=mock_result)

            from nanobananapro_mcp.server import edit_image

            result = await edit_image(
                prompt="Make it brighter",
                image_path="/tmp/test.png",
                seed=54321,
            )

            mock_client.edit_image.assert_called_once()
            call_kwargs = mock_client.edit_image.call_args.kwargs
            assert call_kwargs.get("seed") == 54321

    @pytest.mark.asyncio
    async def test_compose_images_accepts_seed(self):
        """compose_images should accept optional seed parameter."""
        with patch("nanobananapro_mcp.server.get_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client
            mock_result = Mock()
            mock_result.text = "Composed image"
            mock_result.image_data = b"fake_data"
            mock_result.mime_type = "image/png"
            mock_result.grounding_metadata = None
            mock_client.compose_images = AsyncMock(return_value=mock_result)

            from nanobananapro_mcp.server import compose_images

            result = await compose_images(
                prompt="Combine these",
                image_paths=["/tmp/a.png", "/tmp/b.png"],
                seed=99999,
            )

            mock_client.compose_images.assert_called_once()
            call_kwargs = mock_client.compose_images.call_args.kwargs
            assert call_kwargs.get("seed") == 99999


class TestSeedValidation:
    def test_validate_seed_accepts_valid_int(self):
        from nanobananapro_mcp.utils import validate_seed

        assert validate_seed(12345) == 12345
        assert validate_seed(0) == 0
        assert validate_seed(2147483647) == 2147483647

    def test_validate_seed_accepts_none(self):
        from nanobananapro_mcp.utils import validate_seed

        assert validate_seed(None) is None

    def test_validate_seed_rejects_negative(self):
        from nanobananapro_mcp.utils import validate_seed

        with pytest.raises(ValueError, match="non-negative"):
            validate_seed(-1)

    def test_validate_seed_rejects_too_large(self):
        from nanobananapro_mcp.utils import validate_seed

        with pytest.raises(ValueError, match="exceed"):
            validate_seed(2147483648)

    def test_validate_seed_rejects_non_integer(self):
        from nanobananapro_mcp.utils import validate_seed

        with pytest.raises(ValueError, match="integer"):
            validate_seed("12345")

        with pytest.raises(ValueError, match="integer"):
            validate_seed(3.14)


class TestClientSeedParameter:
    """Tests for seed parameter in client methods."""

    @pytest.mark.asyncio
    async def test_client_generate_image_accepts_seed(self):
        """GeminiImageClient.generate_image should accept seed parameter."""
        with patch("nanobananapro_mcp.client.genai") as mock_genai:
            mock_client = Mock()
            mock_genai.Client.return_value = mock_client
            mock_response = Mock()
            mock_response.parts = [Mock(text="test", inline_data=None)]
            mock_aio = Mock()
            mock_aio.models.generate_content = AsyncMock(return_value=mock_response)
            mock_client.aio = mock_aio

            from nanobananapro_mcp.client import GeminiImageClient

            client = GeminiImageClient(api_key="test-key")
            await client.generate_image(prompt="A sunset", seed=12345)

            # Verify the method was called (seed handling is internal)
            mock_aio.models.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_client_edit_image_accepts_seed(self):
        """GeminiImageClient.edit_image should accept seed parameter."""
        import tempfile
        from PIL import Image

        # Create a temporary test image
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            img = Image.new("RGB", (100, 100), color="red")
            img.save(f.name)
            temp_path = f.name

        with patch("nanobananapro_mcp.client.genai") as mock_genai:
            mock_client = Mock()
            mock_genai.Client.return_value = mock_client
            mock_response = Mock()
            mock_response.parts = [Mock(text="test", inline_data=None)]
            mock_aio = Mock()
            mock_aio.models.generate_content = AsyncMock(return_value=mock_response)
            mock_client.aio = mock_aio

            from nanobananapro_mcp.client import GeminiImageClient

            client = GeminiImageClient(api_key="test-key")
            await client.edit_image(prompt="Make it brighter", image_path=temp_path, seed=54321)

            mock_aio.models.generate_content.assert_called_once()

        # Cleanup
        import os
        os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_client_compose_images_accepts_seed(self):
        """GeminiImageClient.compose_images should accept seed parameter."""
        import tempfile
        from PIL import Image

        # Create temporary test images
        temp_paths = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
                img = Image.new("RGB", (100, 100), color="blue")
                img.save(f.name)
                temp_paths.append(f.name)

        with patch("nanobananapro_mcp.client.genai") as mock_genai:
            mock_client = Mock()
            mock_genai.Client.return_value = mock_client
            mock_response = Mock()
            mock_response.parts = [Mock(text="test", inline_data=None)]
            mock_aio = Mock()
            mock_aio.models.generate_content = AsyncMock(return_value=mock_response)
            mock_client.aio = mock_aio

            from nanobananapro_mcp.client import GeminiImageClient

            client = GeminiImageClient(api_key="test-key")
            await client.compose_images(prompt="Combine", image_paths=temp_paths, seed=99999)

            mock_aio.models.generate_content.assert_called_once()

        # Cleanup
        import os
        for p in temp_paths:
            os.unlink(p)
