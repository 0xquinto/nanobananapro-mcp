"""Integration tests - require GEMINI_API_KEY environment variable."""

import os
import pytest
from pathlib import Path

# Skip all tests if no API key
pytestmark = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set"
)


class TestIntegration:
    @pytest.mark.asyncio
    async def test_generate_simple_image(self, tmp_path):
        from nanobananapro_mcp.server import generate_image

        result = await generate_image(
            prompt="A simple red circle on white background",
            model="flash",
            aspect_ratio="1:1",
            output_path=str(tmp_path / "test.png"),
        )

        assert result["image_base64"] is not None
        assert result["saved_path"] is not None
        assert Path(result["saved_path"]).exists()

    @pytest.mark.asyncio
    async def test_chat_session_flow(self):
        from nanobananapro_mcp.server import (
            start_image_chat,
            continue_image_chat,
            end_image_chat,
        )

        # Start session
        start_result = await start_image_chat(
            initial_prompt="Create a simple blue square",
            model="flash",
        )
        assert "session_id" in start_result

        # Continue session
        continue_result = await continue_image_chat(
            session_id=start_result["session_id"],
            prompt="Add a yellow border",
        )
        assert continue_result["turn_count"] == 2

        # End session
        end_result = await end_image_chat(start_result["session_id"])
        assert end_result["status"] == "ended"
