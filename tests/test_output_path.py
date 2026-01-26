"""Tests for output_path parameter behavior."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from nanobananapro_mcp.server import _result_to_dict, _generate_output_path
from nanobananapro_mcp.client import ImageGenerationResult


def test_result_to_dict_with_output_path_saves_to_specified_path():
    """When output_path is provided, image is saved to that path."""
    result = ImageGenerationResult(
        text="Test image",
        image_data=b"fake image bytes",
        mime_type="image/png",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.png"
        response = _result_to_dict(result, str(output_path))

        assert "image_base64" not in response  # base64 no longer included
        assert response["saved_path"] == str(output_path.absolute())
        assert output_path.read_bytes() == b"fake image bytes"


def test_result_to_dict_without_output_path_saves_to_default():
    """When no output_path, image is saved to default outputs/ directory."""
    result = ImageGenerationResult(
        text="Test image",
        image_data=b"fake image bytes",
        mime_type="image/png",
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock the default output directory
        with patch("nanobananapro_mcp.server.DEFAULT_OUTPUT_DIR", str(tmpdir)):
            response = _result_to_dict(result, output_path=None)

            assert "image_base64" not in response  # base64 no longer included
            assert response["saved_path"] is not None
            assert tmpdir in response["saved_path"]
            # File should exist and contain the image data
            assert Path(response["saved_path"]).read_bytes() == b"fake image bytes"


def test_generate_output_path_creates_directory():
    """_generate_output_path creates the outputs directory if needed."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "outputs"
        assert not output_dir.exists()

        with patch("nanobananapro_mcp.server.DEFAULT_OUTPUT_DIR", str(output_dir)):
            path = _generate_output_path()

            assert output_dir.exists()
            assert path.parent == output_dir
            assert path.name.startswith("image_")
            assert path.suffix == ".png"


def test_generate_output_path_uses_prefix():
    """_generate_output_path respects the prefix parameter."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("nanobananapro_mcp.server.DEFAULT_OUTPUT_DIR", str(tmpdir)):
            path = _generate_output_path(prefix="edited")

            assert path.name.startswith("edited_")
