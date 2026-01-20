import pytest
from unittest.mock import Mock, patch, AsyncMock
import json


class TestGenerateImageTool:
    @pytest.mark.asyncio
    async def test_returns_structured_result(self):
        with patch("nanobananapro_mcp.server.GeminiImageClient") as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_result = Mock()
            mock_result.text = "A beautiful sunset"
            mock_result.image_data = b"fake_png_data"
            mock_result.mime_type = "image/png"
            mock_client.generate_image.return_value = mock_result

            from nanobananapro_mcp.server import generate_image

            result = await generate_image(
                prompt="A sunset over mountains",
                model="flash",
                aspect_ratio="16:9",
            )

            assert "text" in result
            assert "image_base64" in result
            assert result["text"] == "A beautiful sunset"


class TestEditImageTool:
    @pytest.mark.asyncio
    async def test_edit_requires_image_path(self):
        from nanobananapro_mcp.server import edit_image

        with pytest.raises(TypeError):
            await edit_image(prompt="Add a cat")


class TestChatSessionTools:
    @pytest.mark.asyncio
    async def test_start_chat_returns_session_id(self):
        with patch("nanobananapro_mcp.server.session_manager") as mock_manager:
            mock_manager.create_session.return_value = "test-session-123"
            mock_session = Mock()
            mock_result = Mock()
            mock_result.text = "Created infographic"
            mock_result.image_data = b"fake_image"
            mock_result.mime_type = "image/png"
            mock_session.send_message.return_value = mock_result
            mock_manager.get_session.return_value = mock_session

            from nanobananapro_mcp.server import start_image_chat

            result = await start_image_chat(
                initial_prompt="Create an infographic",
                model="pro",
            )

            assert "session_id" in result
            assert result["session_id"] == "test-session-123"
